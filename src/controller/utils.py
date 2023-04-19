from ..model.utils import get_database


async def common_parameters():
    return {"db": get_database()}
