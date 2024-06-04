from domjudge_tool_cli.services.api.v4 import SubmissionsAPI

class CustomSubmissionsAPI(SubmissionsAPI):
    async def submission_files(
        self,
        cid: str,
        id: str,
        filename: str,
    ) -> str:

        path = self.make_resource(f"/contests/{cid}/submissions/{id}/files")
        file_name = f"{filename}_{id}.zip"
        result = await self.get_file(path)

        return file_name, result