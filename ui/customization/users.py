import asyncio
import typer

from typing import List, Dict, Optional

from customization._users import (
    UserExportFormat,
    create_teams_and_users,
    create_category_obj,
    categories_options,
    delete_teams_and_users,
    get_users,
    get_affiliations,
)

from utils.web import get_config


__all__ = [
    "app",
    "UserExportFormat",
    "create_teams_and_users",
    "delete_teams_and_users",
    "get_user",
    "get_users",
]


app = typer.Typer()


def user_list(
    ids: Optional[str] = None,
    team_id: Optional[str] = None,
    format: Optional[UserExportFormat] = None,
    file: Optional[typer.FileBinaryWrite] = typer.Option(
        None,
        help="Export file name",
    ),
):
    """
    Get DOMjudge users info.
    Args:
        ids: User ids.
        team_id: Team id
        format: Export file format.
        file: Export file name.
    """
    user_ids = None
    if ids:
        user_ids = ids.split(",")

    client = get_config()
    return asyncio.run(get_users(client, user_ids, team_id, format, file))


def import_users_teams(
    file: Optional[object],
    category_id: Optional[int] = None,
    affiliation_id: Optional[int] = None,
    user_roles: Optional[List[int]] = None,
    enabled: bool = True,
    format: Optional[UserExportFormat] = None,
    ignore_existing: bool = False,
    delete_existing: bool = False,
    password_length: Optional[int] = None,
    password_pattern: Optional[str] = None,
    new_password: bool = False,
):
    client = get_config()
    return asyncio.run(
        create_teams_and_users(
            client,
            file,
            category_id,
            affiliation_id,
            user_roles,
            enabled,
            format,
            ignore_existing,
            delete_existing,
            password_length,
            password_pattern,
            new_password,
        ),
    )


def get_affiliations_options():
    client = get_config()

    return asyncio.run(get_affiliations(client))
    

def get_categories_options() -> Dict[str, object]:
    client = get_config()

    return asyncio.run(categories_options(client))


def create_category(
    name: str = None,
    sortorder: Optional[str] = None,
    color: Optional[str] = None,
    visible: Optional[bool] = True,
    allow_self_registration: Optional[bool] = False,
):
    client = get_config()

    return asyncio.run(
        create_category_obj(
            client=client,
            name=name,
            sortorder=sortorder,
            color=color,
            visible=visible,
            allow_self_registration=allow_self_registration,
        )
    )