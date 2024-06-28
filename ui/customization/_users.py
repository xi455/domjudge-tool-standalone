from enum import Enum
from typing import Any, Dict, List, Optional, Union

import typer
from tablib import Dataset

from domjudge_tool_cli.models import CreateUser, DomServerClient, User
from domjudge_tool_cli.services.api.v4 import UsersAPI
from domjudge_tool_cli.utils.password import gen_password

from customization.serverices.web import CustomDomServerWebGateway
from utils.web import get_session


def gen_user_dataset(users: List[Any]) -> Dataset:
    dataset = Dataset()
    for idx, user in enumerate(users):
        if idx == 0:
            dataset.headers = user.dict().keys()

        dataset.append(user.dict().values())

    return dataset


class UserExportFormat(str, Enum):
    JSON = "json"
    CSV = "csv"

    def export(
        self,
        users: List[Any],
        file: Optional[typer.FileBinaryWrite] = None,
        name: Optional[str] = None,
    ) -> str:
        dataset = gen_user_dataset(users)
        if file:
            file.write(dataset.export(self.value))
            return file.name
        else:
            if not name:
                name = f"export_users.{self.value}"
            else:
                name = f"{name}.{self.value}"

            with open(name, "w") as f:
                f.write(dataset.export(self.value))
                return name


async def get_users(
    client: DomServerClient,
    ids: Optional[List[str]] = None,
    team_id: Optional[str] = None,
    format: Optional[UserExportFormat] = None,
    file: Optional[typer.FileBinaryWrite] = None,
):
    async with UsersAPI(**client.api_params) as api:
        users = await api.all_users(ids, team_id)

    if ids:
        users = list(filter(lambda obj: obj.id in ids, users))

    if team_id:
        users = list(filter(lambda obj: obj.team_id == team_id, users))

    if format:
        format.export(users, file)

    return users


async def create_team_and_user(
    client: DomServerClient,
    user: Union[CreateUser, User],
    category_id: Optional[int] = None,
    affiliation_id: Optional[int] = None,
    user_roles: Optional[List[int]] = None,
    enabled: bool = True,
    password_length: Optional[int] = None,
    password_pattern: Optional[str] = None,
    new_password: bool = False,
) -> CreateUser:
    if not category_id:
        category_id = client.category_id

    if not user_roles:
        user_roles = client.user_roles

    if not user.password or new_password:
        user.password = gen_password(password_length, password_pattern)

    DomServerWeb = CustomDomServerWebGateway(client.version)
    async with DomServerWeb(**client.api_params) as web:
        await web.login()
        if not affiliation_id and not user.affiliation:
            affiliation_id = client.affiliation_id
        elif user.affiliation:
            affiliation = await web.get_affiliation(user.affiliation)

            if affiliation:
                affiliation_id = affiliation.id
            else:
                name = user.affiliation
                affiliation = await web.create_affiliation(
                    name,
                    name,
                    client.affiliation_country,
                )
                affiliation_id = affiliation.id


        if isinstance(user, User):
            team_id, user_id = await web.update_team(
                user,
                category_id,
                affiliation_id,
                enabled,
            )
            user = CreateUser.from_user(user)
            
        else:
            team_id, user_id = await web.create_team_and_user(
                user,
                category_id,
                affiliation_id,
                enabled,
            )

        await web.set_user_password(user_id, user.password, user_roles, enabled)

        return user


async def create_teams_and_users(
    client: DomServerClient,
    file: Optional[object],
    category_id: Optional[int] = None,
    affiliation_id: Optional[str] = None,
    user_roles: Optional[List[int]] = None,
    enabled: bool = True,
    format: Optional[UserExportFormat] = None,
    ignore_existing: bool = False,
    delete_existing: bool = False,
    password_length: Optional[int] = None,
    password_pattern: Optional[str] = None,
    new_password: bool = False,
) -> None:
    async with UsersAPI(**client.api_params) as api:
        users = await api.all_users()

    existing_users: Dict[str, User] = {it.username: it for it in users}

    if not format:
        format = UserExportFormat.CSV

    if format == UserExportFormat.CSV:
        input_file = file.read().decode("utf-8")

    users = []
    delete_users = []
    dataset = Dataset().load(input_file, format=format.value)

    affiliation_option = await get_affiliations(client)
    affiliation_ids_name_dict = {affiliation.id: affiliation.shortname for affiliation in affiliation_option}

    for item in dataset.dict:
        item["email"] = None if not item.get("email") else item["email"]
        item["affiliation"] = item["affiliation"] if item["affiliation"] else affiliation_ids_name_dict.get(str(affiliation_id))
        
        user = CreateUser(**item)

        username = user.username
        if username in existing_users:
            existing_user = existing_users[username]

            if delete_existing:
                delete_users.append(existing_user.username)

            if ignore_existing:
                typer.echo(f"User {user.username} is ignored")
                continue

            if not delete_existing and not ignore_existing:
                existing_user.update(**item)
                users.append(existing_user)
                continue

        users.append(user)

    if delete_users:
        delete_teams = [
            existing_users[username].team_id
            for username in delete_users
            if existing_users[username].team_id
        ]
        DomServerWeb = CustomDomServerWebGateway(client.version)
        async with DomServerWeb(**client.api_params) as web:
            await web.login()
            typer.echo("Delete existing users.")
            await web.delete_users(delete_users)
            typer.echo("Delete existing teams.")
            await web.delete_teams(delete_teams)

    new_users = []
    with typer.progressbar(users) as progress:
        for user in progress:
            new_user = await create_team_and_user(
                client,
                user,
                category_id,
                affiliation_id,
                user_roles,
                enabled,
                password_length,
                password_pattern,
                new_password,
            )
            new_users.append(new_user)

    if new_users:
        file_name = format.export(new_users, name="import-users-teams-out")
        typer.echo(file_name)


async def delete_teams_and_users(
    client: DomServerClient,
    include: Optional[List[str]] = None,
    exclude: Optional[List[str]] = None,
) -> None:
    default_ignore_users = ["admin", "judgehost", client.username]

    async with UsersAPI(**client.api_params) as api:
        users = await api.all_users()

    existing_users = [it.username for it in users]

    if not exclude:
        exclude = default_ignore_users

    if not include:
        include = existing_users

    if include:
        include = list(
            filter(
                lambda it: it not in default_ignore_users,
                include,
            )
        )

    include_teams = [it.team_id for it in users if it.username in include]
    exclude_teams = [it.team_id for it in users if it.username in exclude]

    DomServerWeb = CustomDomServerWebGateway(client.version)
    async with DomServerWeb(**client.api_params) as web:
        await web.login()
        typer.echo("Delete users.")
        await web.delete_users(include, exclude)
        typer.echo("Delete teams.")
        await web.delete_teams(include_teams, exclude_teams)


async def get_affiliations(client: DomServerClient):
    DomServerWeb = CustomDomServerWebGateway(client.version)
    async with DomServerWeb(**client.api_params) as web:
        await web.login()

        return await web.get_affiliations()
    

async def categories_options(
    client: DomServerClient,
) -> Dict[str, object]:
    DomServerWeb = CustomDomServerWebGateway(client.version)
    
    async with DomServerWeb(**client.api_params) as web:
        await web.login()
        categorys = await web.get_categorys()

        return {category.name: category for category in categorys}
    

async def language_options(
    client: DomServerClient,
) -> Dict[str, object]:
    DomServerWeb = CustomDomServerWebGateway(client.version)
    
    async with DomServerWeb(**client.api_params) as web:
        await web.login()
        languages = await web.get_languages()

        return {language.name: language for language in languages}
    

async def create_category_obj(
    client: DomServerClient,
    name: str,
    sortorder: Optional[str] = None,
    color: Optional[str] = None,
    visible: Optional[bool] = True,
    allow_self_registration: Optional[bool] = False,
):
    web = await get_session(client)
    return await web.create_category(
        name,
        sortorder,
        color,
        visible,
        allow_self_registration,
    )