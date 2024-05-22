from kibun.backend.ply import get_context_ply
from kibun.backend.ply import request_ply


async def single_ply_executor(semaphore, task, browser):
    async with semaphore:
        endpoint = task.endpoint(**task.endpoint_kwargs)

        context = await get_context_ply(browser, task.proxy)

        result = await request_ply(context, endpoint, task)

        await context.close()

        return result
