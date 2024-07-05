from typing import Type

from domjudge_tool_cli.services.web.base import BaseDomServerWeb
from domjudge_tool_cli.services.web import DomServerWebGateway

from customization.serverices.web import v7, v8

__all__ = [
    "CustomDomServerWebGateway",
]


# TODO: Generics
class CustomDomServerWebGateway(DomServerWebGateway):
    version_client = {
        "7.3.2": v7.CustomDomServerWeb,
        "7.3.4": v7.CustomDomServerWeb,
        "8.1.3": v8.CustomDomServerWeb,
    }

    def __new__(cls, version: str) -> Type[BaseDomServerWeb]:
        return super().__new__(cls, version)
