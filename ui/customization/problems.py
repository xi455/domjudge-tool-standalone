import asyncio

from typing import List, Optional

from customization._problems import problems_info, download_problems_zips
from utils.web import get_config
        
def download_problems(
    exclude: Optional[List[str]] = None,
    only: Optional[List[str]] = None,
    folder: Optional[str] = None,
):
    if len(exclude) == 1 and isinstance(exclude[0], str):
        exclude = exclude[0].split(",")

    if len(only) == 1 and isinstance(only[0], str):
        only = only[0].split(",")

    client = get_config()
    return asyncio.run(download_problems_zips(client, exclude, only, folder))


def get_problems_info():

    client = get_config()
    return asyncio.run(problems_info(client))