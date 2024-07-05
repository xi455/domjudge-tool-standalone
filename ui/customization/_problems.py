import os
import io
import zipfile

from typing import List, Optional

from domjudge_tool_cli.models import DomServerClient
from customization.serverices.web import CustomDomServerWebGateway

from utils.web import get_session


async def download_problems_zips(
    client: DomServerClient,
    exclude: Optional[List[str]] = None,
    only: Optional[List[str]] = None,
    folder: Optional[str] = None,
) -> None:
    if not folder:
        folder = "export_problems"

    DomServerWeb = CustomDomServerWebGateway(client.version)
    
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
        

async def problems_info(client):
    web = await get_session(client=client)
    objs = await web.get_problems(exclude=list())

    return objs if objs is not None else list()