from kibun.backend.aio.utils import make_request_aio
from kibun.task import create_task_result
from kibun.logger import logger
from kibun import constants
from kibun import utils
import traceback
import asyncio
import json


async def request_aio(session, endpoint, task):
    success = False
    status = None
    attempts = 0

    while attempts < task.max_attempts:
        content, status = await make_request_aio(
            session,
            endpoint,
            params=task.params,
            method=task.method,
            proxy=task.proxy,
        )

        if status is None or status in task.allowed_status:
            try:
                # Sometimes decode can fail
                # Hence we do that in try/except block
                if task.response_format == constants.RESPONSE_HTML:
                    decoded_content = content.decode("utf-8")
                    domain = utils.get_website_address(endpoint)

                    if "<head>" not in decoded_content:
                        continue

                    if domain not in decoded_content:
                        continue

                if task.save_path:
                    await utils.utils.save_text_to_file(
                        task.save_path, content.decode("utf-8")
                    )

                else:
                    if task.response_format == constants.RESPONSE_JSON:
                        content = json.loads(content)

                    result = await task.parser(content, **task.parser_kwargs)
                    await task.process(result, **task.process_kwargs)

                success = True
                break

            except Exception as _:
                logger.error(
                    f"Request {endpoint} failed, retrying ({attempts})"
                )

                # Dump full output for debuging
                # TODO: make this optional (?)
                traceback.print_exc()

        if status in task.done_status:
            break

        if status in task.delete_status:
            if task.delete is not None:
                await task.delete(**task.delete_kwargs)
                success = True

            break

        attempts += 1

        logger.error(f"Request failed {endpoint} {status} ({attempts})")

    if task.sleep > 0:
        await asyncio.sleep(task.sleep)

    if not success:
        task.fails += 1

    return create_task_result(task, success, endpoint, status)
