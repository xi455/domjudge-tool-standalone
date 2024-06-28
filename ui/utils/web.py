import streamlit as st
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