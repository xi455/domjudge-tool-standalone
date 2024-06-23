import os
import io
import asyncio
import zipfile

from typing import List, Optional

from domjudge_tool_cli.commands.general import general_state, get_or_ask_config
# from domjudge_tool_cli.commands.problems._problems import download_problems_zips

from domjudge_tool_cli.models import DomServerClient
from domjudge_tool_cli.services.web import DomServerWebGateway

from ._problems import problems_info

async def download_problems_zips(
    client: DomServerClient,
    exclude: Optional[List[str]] = None,
    only: Optional[List[str]] = None,
    folder: Optional[str] = None,
) -> None:
    if not folder:
        folder = "export_problems"

    DomServerWeb = DomServerWebGateway(client.version)
    
    async with DomServerWeb(**client.api_params) as web:
        await web.login()
        problems = await web.get_problems(exclude, only)

        if len(problems) == 0:
            return folder, None
        
        with io.BytesIO() as f:
            with zipfile.ZipFile(f, 'w') as zipf:
                for problem in problems:
                    export_file_path = problem.export_file_path
                    disk_file_path = f"{folder}.zip"
                    disk_file_path = os.path.join(folder, f"{problem.id}.zip")
                    if not export_file_path:
                        continue

                    r = await web.get(export_file_path)
                    zipf.writestr(disk_file_path, r.content)

            return folder, f.getvalue()
        
def download_problems(
    exclude: Optional[List[str]] = None,
    only: Optional[List[str]] = None,
    folder: Optional[str] = None,
):
    if len(exclude) == 1 and isinstance(exclude[0], str):
        exclude = exclude[0].split(",")

    if len(only) == 1 and isinstance(only[0], str):
        only = only[0].split(",")

    client = get_or_ask_config(general_state["config"])
    return asyncio.run(download_problems_zips(client, exclude, only, folder))


def get_problems_info():
    client = get_or_ask_config(general_state["config"])

    return asyncio.run(problems_info(client))