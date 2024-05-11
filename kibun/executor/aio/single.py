from kibun.backend.aio import get_session_aio
from kibun.backend.aio import request_aio


async def single_aio_executor(semaphore, task):
    async with semaphore:
        endpoint = task.endpoint(**task.endpoint_kwargs)
        session = get_session_aio(task.proxy_type, task.proxy_timeout)

        result = await request_aio(session, endpoint, task)

        await session.close()
        return result
