from typing import Dict, List, Optional

import os
import shutil
import base64
import zipfile
import aiofiles
import aiofiles.os
import asyncio

from domjudge_tool_cli.models import DomServerClient
from domjudge_tool_cli.services.api.v4 import (
    ProblemsAPI,
    TeamsAPI,
)
from domjudge_tool_cli.commands.submissions._submissions import (
    index_by_id,
    judgement_submission_mapping,
)

from customization.serverices.api.v4 import CustomSubmissionsAPI


def file_path(
    cid: str,
    mode: int,
    team: object,
    problem: object,
):
    """
    Constructs the file path based on the given parameters.

    Parameters:
    - cid (str): The contest ID.
    - mode (int): The mode indicating the file path structure.
    - team (Team): The team object.
    - problem (Problem): The problem object.

    Returns:
    - filepath (str): The constructed file path.
    """
    if mode == 1:
        filepath = f"team_{team.name}/problem_{problem.short_name}"
    elif mode == 2:
        filepath = f"problem_{problem.short_name}/team_{team.name}"
    else:
        filepath = f"contest_{cid}"

    return filepath


async def get_submissions(
    client: DomServerClient,
    cid: str,
    language_id: Optional[str] = None,
) -> Dict[str, object]:
    """
    Retrieve submissions for a given contest and optional language.

    Args:
        client (DomServerClient): The DomServerClient instance used for API communication.
        cid (str): The contest ID.
        language_id (Optional[str], optional): The language ID. Defaults to None.

    Returns:
        Dict[str, object]: A dictionary mapping team-problem options to submissions.

    """
    async with CustomSubmissionsAPI(**client.api_params) as api:
        submissions = await api.all_submissions(cid, language_id=language_id)


        async with TeamsAPI(**client.api_params) as team_api:
            teams = await team_api.all_teams(cid)
            teams_mapping = index_by_id(teams)


        async with ProblemsAPI(**client.api_params) as problem_api:
            problems = await problem_api.all_problems(cid)
            problems_mapping = index_by_id(problems)


        async def get_team_problem_option(submission) -> Dict[str, object]:
            
            if (
                submission.team_id not in teams_mapping
                or submission.problem_id not in problems_mapping
            ):
                return

            team = teams_mapping[submission.team_id]
            problem = problems_mapping[submission.problem_id]

            return {f"{team.display_name} - {problem.short_name}": submission}
        
        tasks = [get_team_problem_option(submission) for submission in submissions]

        data = dict()
        for task in await asyncio.gather(*tasks):
            if task:
                data.update(task)

        return data
    
async def get_submission_source_code(
    client: DomServerClient,
    cid: str,
    id: str,
):
    async with CustomSubmissionsAPI(**client.api_params) as api:
        submissionfile = await api.submission_file_name(
            cid,
            id,
        )

        encoded_str = submissionfile.source
        encoded_str = encoded_str.replace("\n", "")

        # 解碼Base64
        decoded_bytes = base64.b64decode(encoded_str)
        decoded_str = decoded_bytes.decode('utf-8')

        return decoded_str

async def download_submission_files(
    client: DomServerClient,
    cid: str,
    id: str,
):
    judgement_mapping = await judgement_submission_mapping(client, cid)
    async with CustomSubmissionsAPI(**client.api_params) as api:

        submission_file = await api.submission_file_name(cid, id)
        submission_filename = submission_file.filename.split(".")[0]

        judgement_name = judgement_mapping.get(id)

        submission_filename = f"{submission_filename}_{judgement_name}"
        
        return await api.submission_files(
            cid,
            id,
            submission_filename,
        )
    
async def get_submission_dirs(
    client: DomServerClient,
    cid: str,
    submission_ids: List[str],
    mode: int,
):
    """Get the file paths for the submissions.

    Args:
        client (DomServerClient): The DomServerClient object.
        cid (str): The contest ID.
        submission_ids (List[str]): The list of submission IDs.
        mode (int): The mode.

    Returns:
        List[str]: The list of file paths for the submissions.
    """
    async with CustomSubmissionsAPI(**client.api_params) as api:

        paths = list()
        for id in submission_ids:
            submission = await api.submission(cid, id)

            async with TeamsAPI(**client.api_params) as team_api:
                team = await team_api.team(cid, submission.team_id)

            async with ProblemsAPI(**client.api_params) as problem_api:
                problem = await problem_api.problem(cid, submission.problem_id)
        
            paths.append(file_path(cid, mode, team, problem))

    return paths


async def download_submission_zip(
    client: DomServerClient,
    cid: str,
    submission_ids: List[str],
    mode: int,
):
    
    """
    Downloads and zips the submissions identified by the given submission IDs.

    Args:
        client (DomServerClient): The DomServerClient object used for making API requests.
        cid (str): The contest ID.
        submission_ids (List[str]): A list of submission IDs to download.
        mode (int): The mode of the submissions.

    Returns:
        bytes: The zipped file containing the downloaded submissions.
    """

    # 創建一個臨時目錄
    async with aiofiles.tempfile.TemporaryDirectory() as temp_dir:
        # 在臨時目錄中創建一個新的目錄

        paths = await get_submission_dirs(
            client=client,
            cid=cid,
            submission_ids=submission_ids,
            mode=mode,
        )

        # 創建新的目錄
        for index in range(len(paths)):
            paths[index] = os.path.join(temp_dir, paths[index])
            os.makedirs(paths[index], exist_ok=True)

        submissions_list = [download_submission_files(
            client=client,
            cid=cid,
            id=id,
        ) for id in submission_ids]
        results = await asyncio.gather(*submissions_list)

        for path, result in zip(paths, results):
            filename, submission = result
            zip_path = os.path.join(path, filename)    
            async with aiofiles.open(zip_path, "wb") as f:
                await f.write(submission)

            # 解壓縮文件
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(path)

            os.remove(zip_path)

        zip_file_path = shutil.make_archive(temp_dir, 'zip', temp_dir)

        async with aiofiles.open(zip_file_path, "rb") as f:
            zip_file = await f.read()

        return zip_file


async def download_contest_files(
    client: DomServerClient,
    cid: str,
    mode: int,
):
    """
    Downloads contest files for a given contest ID.

    Args:
        client (DomServerClient): The DomServerClient object used for API communication.
        cid (str): The contest ID.
        mode (int): The mode of the contest files.

    Returns:
        bytes: The downloaded contest files as a zip archive.
    """
    judgement_mapping = await judgement_submission_mapping(client, cid)
    async with CustomSubmissionsAPI(**client.api_params) as api:
        submissions = await api.all_submissions(cid)

        async with TeamsAPI(**client.api_params) as team_api:
            teams = await team_api.all_teams(cid)
            teams_mapping = index_by_id(teams)

        async with ProblemsAPI(**client.api_params) as problem_api:
            problems = await problem_api.all_problems(cid)
            problems_mapping = index_by_id(problems)

        async def get_source_codes(submission) -> None:
            id = submission.id
            
            if (
                submission.team_id not in teams_mapping
                or submission.problem_id not in problems_mapping
            ):
                return

            team = teams_mapping[submission.team_id]
            problem = problems_mapping[submission.problem_id]
            judgement_name = judgement_mapping.get(id)

            path = file_path(cid, mode, team, problem)
            
            new_dir = os.path.join(temp_dir, path)
            os.makedirs(new_dir, exist_ok=True)

            file_name, result = await api.submission_files(
                cid,
                id,
                judgement_name,            
            )

            zip_path = os.path.join(new_dir, file_name)
            async with aiofiles.open(zip_path, "wb") as f:
                await f.write(result)

            # 解壓縮文件
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(new_dir)

            os.remove(zip_path)

        # 創建一個臨時目錄
        async with aiofiles.tempfile.TemporaryDirectory() as temp_dir:
            # 在臨時目錄中創建一個新的目錄
    
            tasks = [get_source_codes(submission) for submission in submissions]
            await asyncio.gather(*tasks)

            # 將臨時目錄壓縮為zip文件
            zip_file_path = shutil.make_archive(temp_dir, 'zip', temp_dir)

            with open(zip_file_path, "rb") as f:
                zip_file = f.read()

        return zip_file