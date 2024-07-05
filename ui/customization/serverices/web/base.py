from abc import ABC, abstractmethod
from typing import List, Optional, Tuple

from domjudge_tool_cli.models import Affiliation, CreateUser, ProblemItem, User
from domjudge_tool_cli.services.api_client import WebClient

from customization.models import Contest, Language, Category


class CustomBaseDomServerWeb(WebClient, ABC):
    @abstractmethod
    async def login(self) -> None:
        ...

    @abstractmethod
    async def create_team_and_user(
        self,
        user: CreateUser,
        category_id: int,
        affiliation_id: int,
        enabled: bool = True,
    ) -> Tuple[str, str]:
        raise NotImplemented

    @abstractmethod
    async def update_team(
        self,
        user: User,
        category_id: int,
        affiliation_id: int,
        enabled: bool = True,
    ) -> Tuple[str, str]:
        raise NotImplemented

    @abstractmethod
    async def set_user_password(
        self,
        user_id: str,
        password: str,
        user_roles: List[int],
        enabled: bool = True,
    ) -> None:
        ...

    @abstractmethod
    async def delete_users(
        self,
        include: List[str] = None,
        exclude: List[str] = None,
    ) -> None:
        """

        Args:
            include: list of username.
            exclude: list of username.
        """
        ...

    @abstractmethod
    async def delete_teams(
        self,
        include: List[str] = None,
        exclude: List[str] = None,
    ) -> None:
        """

        Args:
            include: list of team id.
            exclude: list of team id.
        """
        ...

    @abstractmethod
    async def create_affiliation(
        self,
        shortname: str,
        name: str,
        country: str = "TWN",
    ) -> Affiliation:
        raise NotImplemented

    @abstractmethod
    async def get_affiliations(self) -> List[Affiliation]:
        raise NotImplemented

    @abstractmethod
    async def get_affiliation(self, name: str) -> Optional[Affiliation]:
        raise NotImplemented

    @abstractmethod
    async def get_problems(
        self,
        exclude: Optional[List[str]] = None,
        only: Optional[List[str]] = None,
    ) -> List[ProblemItem]:
        raise NotImplemented
    
    @abstractmethod
    async def get_contests(
        self,
    ) -> List[Contest]:
        raise NotImplemented
    
    @abstractmethod
    async def get_languages(
        self,
    ) -> List[Language]:
        raise NotImplemented
    
    
    @abstractmethod
    async def get_categorys(
        self,
    ) -> List[Category]:
        raise NotImplemented