from typing import Any, Dict, List, Optional

import os
import typer
import shutil
import aiofiles
import aiofiles.os
import asyncio
from tablib import Dataset

from domjudge_tool_cli.models import DomServerClient, Submission
from domjudge_tool_cli.services.api.v4 import (
    JudgementAPI,
    JudgementTypeAPI,
    ProblemsAPI,
    SubmissionsAPI,
    TeamsAPI,
    UsersAPI,
)

from customization.serverices.api.v4 import CustomSubmissionsAPI

from itertools import chain


def gen_submission_dataset(submissions: List[Any]) -> Dataset:
    dataset = Dataset()
    for idx, submission in enumerate(submissions):
        if idx == 0:
            dataset.headers = submission.dict().keys()

        dataset.append(submission.dict().values())

    return dataset


def print_submissions_table(submissions: List[Submission]):
    dataset = gen_submission_dataset(submissions)
    # ["id", "team_id", "problem_id", "language_id",
    # "files", "entry_point", "time", "contest_time", "externalid"]
    for rm_key in ["externalid", "contest_time"]:
        del dataset[rm_key]
    typer.echo(dataset.export("cli", tablefmt="simple"))


def index_by_id(objs):
    data = dict()
    for obj in objs:
        data[obj.id] = obj
    return data


def file_path(cid, mode, team, problem):
    if mode == 1:
        filepath = f"team_{team.name}/problem_{problem.short_name}"
    elif mode == 2:
        filepath = f"problem_{problem.short_name}/team_{team.name}"
    else:
        filepath = f"contest_{cid}"

    return filepath


async def judgement_submission_mapping(
    client: DomServerClient,
    cid: str,
) -> Dict[str, str]:
    async with JudgementTypeAPI(**client.api_params) as api:
        judgement_types = await api.all_judgement_types(cid)

    async with JudgementAPI(**client.api_params) as api:
        judgements = await api.all_judgements(cid)

    judgement_type_mapping = {
        item.id: str(item.name).lower().replace(" ", "_") for item in judgement_types
    }
    return {
        item.submission_id: judgement_type_mapping.get(item.judgement_type_id)
        for item in judgements
    }


async def get_submissions(
    client: DomServerClient,
    cid: str,
) -> Dict[str, object]:
    async with CustomSubmissionsAPI(**client.api_params) as api:
        submissions = await api.all_submissions(cid)

        # Submission(language_id='python3', time='2023-11-20T14:10:05.726+08:00', contest_time='498:35:05.726', id='42389', externalid=None, team_id='1945', problem_id='628', entry_point='', files=[{'href': 'contests/108/submissions/42389/files', 'mime': 'application/zip'}], submission_id=None, filename=None, source=None)

        async with TeamsAPI(**client.api_params) as team_api:
            teams = await team_api.all_teams(cid)
            teams_mapping = index_by_id(teams)

            # '1954': Team(group_ids=['48'], affiliation='112校外讀', nationality='TWN', id='1954', icpc_id=None, name='202309056', display_name='吳柏郁', organization_id='298', members=None)

        async with ProblemsAPI(**client.api_params) as problem_api:
            problems = await problem_api.all_problems(cid)
            problems_mapping = index_by_id(problems)

            # '652': Problem(ordinal=7, id='652', short_name='U511_232_10970---Big-Chocolate', label='U511_232_10970---Big-Chocolate', time_limit=1, externalid='U511_232_10970---Big-Chocolate', name='10970 - Big Chocolate', rgb=None, color=None, test_data_count=6), 

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

async def download_submission_files(
    client: DomServerClient,
    cid: str,
    id: str,
):
    judgement_mapping = await judgement_submission_mapping(client, cid)
    async with CustomSubmissionsAPI(**client.api_params) as api:

        async with TeamsAPI(**client.api_params) as team_api:
            teams = await team_api.all_teams(cid)
            teams_mapping = index_by_id(teams)

            # '1954': Team(group_ids=['48'], affiliation='112校外讀', nationality='TWN', id='1954', icpc_id=None, name='202309056', display_name='吳柏郁', organization_id='298', members=None)

        async with ProblemsAPI(**client.api_params) as problem_api:
            problems = await problem_api.all_problems(cid)
            problems_mapping = index_by_id(problems)

            # '652': Problem(ordinal=7, id='652', short_name='U511_232_10970---Big-Chocolate', label='U511_232_10970---Big-Chocolate', time_limit=1, externalid='U511_232_10970---Big-Chocolate', name='10970 - Big Chocolate', rgb=None, color=None, test_data_count=6), 

        submission = await api.submission(cid, id)
        submission_file = await api.submission_file_name(cid, id)

        team = teams_mapping[submission.team_id]
        problem = problems_mapping[submission.problem_id]

        submission_filename = submission_file.filename.split(".")[0]
        judgement_name = judgement_mapping.get(id)

        submission_filename = f"{team.display_name}_{problem.short_name}_{submission_filename}_{judgement_name}"

        return await api.submission_files(
            cid,
            id,
            submission_filename,
        )
    

async def download_submission_zip(
    client: DomServerClient,
    cid: str,
    submission_ids: List[str],
):
    # 創建一個臨時目錄
    async with aiofiles.tempfile.TemporaryDirectory() as temp_dir:
        # 在臨時目錄中創建一個新的目錄
        
        submissions_list = [download_submission_files(
            client=client,
            cid=cid,
            id=id,
        ) for id in submission_ids]
        results = await asyncio.gather(*submissions_list)

        for result in results:
            filename, submission = result
            py_file_path = os.path.join(temp_dir, filename)
            async with aiofiles.open(f"{py_file_path}.py", "wb") as f:
                await f.write(submission)

        zip_file_path = shutil.make_archive(temp_dir, 'zip', temp_dir)

        async with aiofiles.open(zip_file_path, "rb") as f:
            zip_file = await f.read()

        return zip_file


async def download_contest_files(
    client: DomServerClient,
    cid: str,
    mode: int,
):
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

            filename, result = await api.submission_files(
                cid,
                id,
                judgement_name,            
            )

            py_file_path = os.path.join(new_dir, filename)

            async with aiofiles.open(f"{py_file_path}.py", "wb") as f:
                await f.write(result)

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