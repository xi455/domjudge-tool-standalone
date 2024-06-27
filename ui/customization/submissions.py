import asyncio
from typing import Dict, List, Optional

import typer

from domjudge_tool_cli.models import DomServerClient

from customization.serverices.web import DomServerWebGateway
from utils.web import get_config

from ._submissions import (
    download_contest_files,
    get_submissions,
    download_submission_zip,
    get_submission_source_code,
)

app = typer.Typer()


def submission_list(
    cid: str,
    language_id: Optional[str] = None,
):
    """
    Console log submissions.
    Args:
        cid: Contest id.
        language_id: Language id.
    """

    client = get_config()
    return asyncio.run(get_submissions(client, cid, language_id))


def submission_file(
    cid: str,
    submission_ids: Optional[List[str]],
    mode: int,
):
    """
    Download a submission source code files.
    Args:
        cid: Contest id.
        submission_ids: Submission id.
        mode: Output path format mode.
        path: Output path.
        strict:
        is_extract: unzip file if true.
    """
    
    client = get_config()
    return asyncio.run(download_submission_zip(client, cid, submission_ids, mode))


def contest_files(
    cid: str,
    mode: int,
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
    
    client = get_config()
    return asyncio.run(
        download_contest_files(
            client,
            cid,
            mode,
        )
    )


async def contest_options(
    client: DomServerClient,
) -> Dict[str, object]:
    DomServerWeb = DomServerWebGateway(client.version)
    
    async with DomServerWeb(**client.api_params) as web:
        await web.login()
        contests = await web.get_contests()

        return {contest.name: contest for contest in contests}


async def language_options(
    client: DomServerClient,
) -> Dict[str, object]:
    DomServerWeb = DomServerWebGateway(client.version)
    
    async with DomServerWeb(**client.api_params) as web:
        await web.login()
        languages = await web.get_languages()

        return {language.name: language for language in languages}


def get_content_options() -> Dict[str, object]:
    client = get_config()

    return asyncio.run(contest_options(client))


def get_language_options() -> Dict[str, object]:
    client = get_config()

    return asyncio.run(language_options(client))

def view_submission(
    cid: str,
    id: str,
) -> None:
    """
    View submission.
    """
    client = get_config()

    return asyncio.run(get_submission_source_code(client, cid, id))