from domjudge_tool_cli.services.web import DomServerWebGateway

async def get_session(client):
    DomServerWeb = DomServerWebGateway(client.version)
    web = DomServerWeb(**client.api_params)
    await web.login()
    
    return web