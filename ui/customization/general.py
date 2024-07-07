import typer
import asyncio

from typing import Optional

from domjudge_tool_cli.models import DomServerClient
from domjudge_tool_cli.commands.general._check import (
    check_login_website,
    get_version,
)


def check(
    host: Optional[str],
    username: Optional[str],
    password: Optional[str],
    version: Optional[str],
    api_version: Optional[str],
    disable_ssl: Optional[bool] = False,
    timeout: Optional[float] = None,
    max_connections: Optional[int] = None,
    max_keepalive_connections: Optional[int] = None,
) -> DomServerClient:

    if not all([host, username, password, version]):
        raise ValueError("請提供網址、帳號、密碼、與版本資訊。")

    client = DomServerClient(
        host=host,
        username=username,
        password=password,
        disable_ssl=disable_ssl or False,
        timeout=timeout,
        max_connections=max_connections,
        max_keepalive_connections=max_keepalive_connections,
        version=version,
        api_version=api_version,
    )

    if client:
        typer.echo(f"Try to connect {client.host}.")
        asyncio.run(get_version(client))
        typer.echo(f"Try to test {client.host}.")
        asyncio.run(check_login_website(client))

    return client