import re
from typing import Dict, List, Optional

import typer
from tablib import Dataset

from domjudge_tool_cli.models import CreateUser, DomServerClient, User
from domjudge_tool_cli.services.api.v4 import UsersAPI
from domjudge_tool_cli.commands.users._users import create_team_and_user, UserExportFormat

from customization.serverices.web import CustomDomServerWebGateway
from customization._options import get_affiliations_options

from utils.web import get_session


async def get_users(
    client: DomServerClient,
    ids: Optional[List[str]] = None,
    team_id: Optional[str] = None,
) -> List[User]:
    async with UsersAPI(**client.api_params) as api:
        users = await api.all_users(ids, team_id)

    if ids:
        users = list(filter(lambda obj: obj.id in ids, users))

    if team_id:
        users = list(filter(lambda obj: obj.team_id == team_id, users))

    return users

async def create_teams_and_users(
    client: DomServerClient,
    file: Optional[object],
    category_id: Optional[str] = None,
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

    affiliation_option = await get_affiliations_options(client)
    affiliation_ids_name_dict = {affiliation.id: affiliation.shortname for affiliation in affiliation_option}

    for item in dataset.dict:
        if not re.match(r'^[0-9a-zA-Z_-]+$', item["username"]):
            raise ValueError("Username Error May only contain [a-zA-Z0-9_-].")
        
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

        with open(file_name, "r") as f:
            return f.read()    
    
async def create_category_obj(
    client: DomServerClient,
    name: str,
    sortorder: Optional[str] = None,
    color: Optional[str] = None,
    visible: Optional[bool] = True,
    allow_self_registration: Optional[bool] = False,
):
    web = await get_session(client)
    await web.create_category(
        name,
        sortorder,
        color,
        visible,
        allow_self_registration,
    )