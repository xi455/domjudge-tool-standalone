from domjudge_tool_cli.services.web import DomServerWebGateway

async def get_session(client):
    """
    Creates and returns a session object for interacting with the DomServerWeb API.

    Args:
        client: The client object used to connect to the DomServerWeb API.

    Returns:
        The session object for interacting with the DomServerWeb API.
    """
    DomServerWeb = DomServerWebGateway(client.version)
    web = DomServerWeb(**client.api_params)
    await web.login()
    
    return web