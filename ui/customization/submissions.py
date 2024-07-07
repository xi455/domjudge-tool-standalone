import asyncio
from typing import ByteString, Dict, List, Optional

from customization._submissions import (
    get_submissions,
    get_submission_source_code,
    download_contest_files,
    download_submission_zip,
)

from utils.web import get_config


def submission_list(
    cid: str,
    language_id: Optional[str] = None,
) -> Dict[str, object]:
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
) -> ByteString:
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
) -> ByteString:
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

def view_submission(
    cid: str,
    id: str,
) -> str:
    """
    View submission.
    """
    client = get_config()

    return asyncio.run(get_submission_source_code(client, cid, id))