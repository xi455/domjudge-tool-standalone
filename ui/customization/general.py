import typer
import asyncio

from typing import Optional
from pydantic import HttpUrl

from domjudge_tool_cli.models import DomServerClient
from domjudge_tool_cli.commands.general._check import (
    check_login_website,
    get_version,
)


def create_config(
    host: HttpUrl,
    username: str,
    password: str,
    version: str,
    api_version: str,
    disable_ssl: bool = False,
    timeout: Optional[float] = None,
    max_connections: Optional[int] = None,
    max_keepalive_connections: Optional[int] = None,
) -> DomServerClient:

    dom_server = DomServerClient(
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
    with open("domserver.json", "wb+") as f:
        f.write(dom_server.json().encode())
        typer.echo("Success config Dom Server.")

    return dom_server


def config(
    host: str,
    username: str,
    password: str,
    version: str,
    api_version: str,
    disable_ssl: Optional[bool] = False,
    timeout: Optional[float] = None,
    max_connections: Optional[int] = None,
    max_keepalive_connections: Optional[int] = None,
):
    create_config(
        host=host,
        username=username,
        password=password,
        version=version,
        api_version=api_version,
        disable_ssl=disable_ssl,
        timeout=timeout,
        max_connections=max_connections,
        max_keepalive_connections=max_keepalive_connections,
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
):

    client = None
    if host and username and password:
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