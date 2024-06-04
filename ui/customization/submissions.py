import asyncio
from typing import Dict, List, Optional

import typer

from domjudge_tool_cli.models import DomServerClient
from domjudge_tool_cli.commands.general import general_state, get_or_ask_config

from customization.serverices.web import DomServerWebGateway

from ._submissions import (
    download_contest_files,
    download_submission_files,
    get_submissions,
    download_submission_zip,
)

app = typer.Typer()


@app.command()
def submission_list(
    cid: str,
    language_id: Optional[str] = None,
    strict: Optional[bool] = False,
    ids: Optional[List[str]] = None,
):
    """
    Console log submissions.
    Args:
        cid: *Contest id.
        language_id:
        strict:
        ids: Submission ids.
    """
    submission_ids = None
    if ids:
        submission_ids = ids.split(",")

    client = get_or_ask_config(general_state["config"])
    asyncio.run(get_submissions(client, cid, language_id, strict, submission_ids))


def submission_file(
    cid: str,
    submission_ids: Optional[List[str]],
    strict: Optional[bool] = False,
):
    """
    Download a submission source code files.
    Args:
        cid: Contest id.
        id: Submission id.
        mode: Output path format mode.
        path: Output path.
        strict:
        is_extract: unzip file if true.
    """
    client = get_or_ask_config(general_state["config"])

    return asyncio.run(download_submission_zip(client, cid, submission_ids))


def contest_files(
    cid: str,
    mode: int = typer.Argument(
        default=2,
        help="""
        Output path format mode:\n
        mode=1: team_name/problem_name/submission_file.
        mode=2: problem_name/team_name/submission_file.
        other: contest_id/submission_file
        """,
    ),
):
    """
    Download a contest all submissions source code files.
    Args:
        cid: Contest id.
        mode: Output path format mode.
        path: Output path.
        strict:
        is_extract: unzip file if true.
    """
    client = get_or_ask_config(general_state["config"])
    return asyncio.run(
        download_contest_files(
            client,
            cid,
            mode,
        )
    )


async def contests_options(
    client: DomServerClient,
) -> Dict[str, object]:
    DomServerWeb = DomServerWebGateway(client.version)
    
    async with DomServerWeb(**client.api_params) as web:
        await web.login()
        contests = await web.get_contests()

        return {contest.name: contest for contest in contests}


def get_content_options() -> Dict[str, object]:
    client = get_or_ask_config(general_state["config"])

    return asyncio.run(contests_options(client))