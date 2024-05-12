from kibun.backend.aio import get_session_aio
from kibun.backend.aio import request_aio


async def single_aio_executor(semaphore, task, session=None):
    local_session = session is None

    async with semaphore:
        endpoint = task.endpoint(**task.endpoint_kwargs)

        # Create local aio session if needed
        if local_session:
            session = get_session_aio(task.proxy_type, task.proxy_timeout)

        result = await request_aio(session, endpoint, task)

        # If we created local session we must close it here as well
        if local_session:
            await session.close()

        return result
