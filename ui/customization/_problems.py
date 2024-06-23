from utils.web import get_session

async def problems_info(client):
    web = await get_session(client=client)
    objs = await web.get_problems(exclude=list())

    return objs if objs is not None else list()