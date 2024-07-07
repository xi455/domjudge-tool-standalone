from typing import Dict, List

from domjudge_tool_cli.models import DomServerClient

from customization.serverices.web import CustomDomServerWebGateway


async def get_contest_options(
    client: DomServerClient,
) -> Dict[str, object]:
    DomServerWeb = CustomDomServerWebGateway(client.version)
    
    async with DomServerWeb(**client.api_params) as web:
        await web.login()
        contests = await web.get_contests()

        return {contest.name: contest for contest in contests}

async def get_language_options(
    client: DomServerClient,
) -> Dict[str, object]:
    DomServerWeb = CustomDomServerWebGateway(client.version)
    
    async with DomServerWeb(**client.api_params) as web:
        await web.login()
        languages = await web.get_languages()

        return {language.name: language for language in languages}
    
async def get_categories_options(
    client: DomServerClient,
) -> Dict[str, object]:
    DomServerWeb = CustomDomServerWebGateway(client.version)
    
    async with DomServerWeb(**client.api_params) as web:
        await web.login()
        categorys = await web.get_categorys()

        return {category.name: category for category in categorys}
    
async def get_affiliations_options(
    client: DomServerClient
) -> List[object]:
    DomServerWeb = CustomDomServerWebGateway(client.version)
    async with DomServerWeb(**client.api_params) as web:
        await web.login()

        return await web.get_affiliations()