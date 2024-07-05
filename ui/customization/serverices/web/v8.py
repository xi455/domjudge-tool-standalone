from enum import Enum
from typing import List, Optional, Tuple

from bs4 import BeautifulSoup

from domjudge_tool_cli.models import Affiliation, CreateUser, ProblemItem, User
from domjudge_tool_cli.services.web.base import _get_input_fields
from domjudge_tool_cli.services.web.v8 import DomServerWeb

from customization.models import Contest, Language, Category
from customization.serverices.web.base import CustomBaseDomServerWeb


class ContestPath(str, Enum):
    LIST = "/jury/contests"
    ADD = "/jury/contests/add"


class LanguagePath(str, Enum):
    LIST = "/jury/languages"


class CategoryPath(str, Enum):
    LIST = "/jury/categories"
    ADD = "/jury/categories/add"


class CustomDomServerWeb(CustomBaseDomServerWeb, DomServerWeb):
    async def login(self) -> None:
        await DomServerWeb.login(self)

    async def create_team_and_user(
        self,
        user: CreateUser,
        category_id: int,
        affiliation_id: int,
        enabled: bool = True,
    ) -> Tuple[str, str]:
        return await DomServerWeb.create_team_and_user(self, user, category_id, affiliation_id, enabled)

    async def update_team(
        self,
        user: User,
        category_id: int,
        affiliation_id: int,
        enabled: bool = True,
    ) -> Tuple[str, str]:
        return await DomServerWeb.update_team(self, user, category_id, affiliation_id, enabled)

    async def set_user_password(
        self,
        user_id: str,
        password: str,
        user_roles: List[int],
        enabled: bool = True,
    ) -> None:
        await DomServerWeb.set_user_password(self, user_id, password, user_roles, enabled)

    async def delete_users(
        self,
        include: List[str] = None,
        exclude: List[str] = None,
    ):
        await DomServerWeb.delete_users(self, include, exclude)

    async def delete_teams(
        self,
        include: List[str] = None,
        exclude: List[str] = None,
    ):
        await DomServerWeb.delete_teams(self, include, exclude)

    async def create_affiliation(
        self,
        shortname: str,
        name: str,
        country: str = "TWN",
    ) -> Affiliation:
        return await DomServerWeb.create_affiliation(self, shortname, name, country)

    async def get_affiliations(self) -> List[Affiliation]:
        return await DomServerWeb.get_affiliations(self)

    async def get_affiliation(self, name: str) -> Optional[Affiliation]:
        return await DomServerWeb.get_affiliation(self, name)

    async def get_problems(
        self,
        exclude: Optional[List[str]] = None,
        only: Optional[List[str]] = None,
    ) -> List[ProblemItem]:
        return await DomServerWeb.get_problems(self, exclude, only)
    
    async def create_category(
        self,
        name: str,
        sortorder: Optional[str],
        color: Optional[str] = None,
        visible: bool = True,
        allow_self_registration: bool = False,
    ) -> Category:
        res = await self.get(CategoryPath.ADD)

        data = {
            **_get_input_fields(res.text),
            "team_category[name]": name,
            "team_category[sortorder]": sortorder if sortorder else "0",
            "team_category[color]": color,
            "team_category[visible]": "1" if visible else "0",
            "team_category[allow_self_registration]": "1" if allow_self_registration else "0",
            "team_category[save]": "",
        }

        res = await self.post(CategoryPath.ADD, body=data)
        assert res.url.path != CategoryPath.ADD, "Category create fail."
        category_id = res.url.path.split("/")[-1]

        return Category(
            id=category_id,
            sortorder=sortorder,
            name=name,
            color=color,
            visible=visible,
            allow_self_registration=allow_self_registration,
        )
    
    async def get_categorys(self) -> List[Category]:
        res = await self.get(CategoryPath.LIST)
        res.raise_for_status()

        soup = BeautifulSoup(res.text, "html.parser")

        objs = []

        table_elements = soup.select(
            "table",
            {
                "class": "data-table table table-sm table-striped dataTable no-footer",
                "id": "DataTables_Table_0",
            },
        )

        tr_elements = table_elements[-1].select("tbody tr")

        for tr_element in tr_elements:

            td_elements = tr_element.select("td")
            category_info_dict = dict()
            
            obj_title = ["id", "icpc_id", "sortorder", "name", "teams", "visible", "allow_self_registration"]
            for index in range(len(obj_title)):

                td = td_elements[index].text.strip()

                if obj_title[index] == "visible" or obj_title[index] == "selfregistration":
                    td = True if td == "yes" else False

                if obj_title[index] == "teams":
                    td = int(td)

                category_info_dict[obj_title[index]] = td

            obj = Category(**category_info_dict)

            objs.append(obj)

        return objs
    
    async def get_contests(self) -> List[Contest]:
        res = await self.get(ContestPath.LIST)
        res.raise_for_status()

        soup = BeautifulSoup(res.text, "html.parser")

        objs = []

        table_elements = soup.select(
            "table",
            {
                "class": "data-table table table-sm table-striped dataTable no-footer",
                "id": "DataTables_Table_0",
            },
        )

        thead_elements = table_elements[-1].select("thead th")
        tr_elements = table_elements[-1].select("tbody tr")

        button_without_title = 2
        for tr_element in tr_elements:

            td_elements = tr_element.select("td")
            contest_info_dict = dict()

            obj_title = ["cid", "name", "shortname", "activate", "start", "end", "process_balloons", "medals", "public", "teams", "problems"]
            for index in range(len(obj_title)):

                thead = (
                    thead_elements[index]
                    .text.strip()
                    .replace("?", "")
                    .replace("# ", "")
                )
                td = td_elements[index].text.strip()
                contest_info_dict[obj_title[index]] = td

            obj = Contest(**contest_info_dict)

            objs.append(obj)

        return objs
    
    async def get_languages(self) -> List[Language]:
        res = await self.get(LanguagePath.LIST)
        res.raise_for_status()

        soup = BeautifulSoup(res.text, "html.parser")

        objs = []

        table_elements = soup.select(
            "table",
            {
                "class": "data-table table table-sm table-striped dataTable no-footer",
                "id": "DataTables_Table_0",
            },
        )

        tr_elements = table_elements[-1].select("tbody tr")

        for tr_element in tr_elements:

            td_elements = tr_element.select("td")
            language_info_dict = dict()
            
            obj_title = ["lid", "external_id", "name", "entrypoint", "allow_submit", "allow_judge", "time_factor", "extensions"]        
            for index in range(len(obj_title)):

                td = td_elements[index].text.strip()

                if obj_title[index] == "entrypoint" or obj_title[index] == "allow_submit" or obj_title[index] == "allow_judge":
                    td = True if td == "yes" else False

                if obj_title[index] == "timefactor":
                    td = int(td)

                language_info_dict[obj_title[index]] = td

            obj = Language(**language_info_dict)

            if obj.allow_submit:
                objs.append(obj)

        all_language = Language(name="All")
        objs.insert(0, all_language)

        return objs