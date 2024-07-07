import asyncio
from typing import Dict, List

from customization._options import (
    get_contest_options,
    get_language_options,
    get_categories_options,
    get_affiliations_options,
)

from utils.web import get_config

def content_options() -> Dict[str, object]:
    client = get_config()

    return asyncio.run(get_contest_options(client))

def language_options() -> Dict[str, object]:
    client = get_config()

    return asyncio.run(get_language_options(client))

def categories_options() -> Dict[str, object]:
    client = get_config()

    return asyncio.run(get_categories_options(client))

def affiliations_options() -> List[object]:
    client = get_config()

    return asyncio.run(get_affiliations_options(client))  