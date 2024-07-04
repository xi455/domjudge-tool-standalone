import streamlit as st

from pathlib import Path
from utils.check import login_required

from domjudge_tool_cli.models import DomServerClient
from customization.serverices.web import CustomDomServerWebGateway

async def get_session(client):
    """
    Creates and returns a session object for interacting with the DomServerWeb API.

    Args:
        client: The client object used to connect to the DomServerWeb API.

    Returns:
        The session object for interacting with the DomServerWeb API.
    """
    DomServerWeb = CustomDomServerWebGateway(client.version)
    web = DomServerWeb(**client.api_params)
    await web.login()
    
    return web


@login_required
def get_config() -> DomServerClient:
    user_info = st.session_state.get("user_info")
    return DomServerClient(**user_info)


@st.cache_data
def get_example_data(file_path):
    """
    Read and return the contents of a file specified by the given file path.
    """
    file_path = Path(file_path)
    with file_path.open("rb") as file:
        file_data = file.read()

    return file_data