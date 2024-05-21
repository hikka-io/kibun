from kibun.logger import logger
import asyncio
import random


async def kibun_loop(tasks, semaphore_number=1):
    semaphore = asyncio.Semaphore(semaphore_number)
    step = 0

    if len(tasks) > 0:
        logger.info(f"Got {len(tasks)} tasks")

    while len(tasks) > 0:
        # Shuffle tasks to make them less predictable
        random.shuffle(tasks)

        result = await asyncio.gather(
            *[
                task.executor(semaphore, task, **task.executor_kwargs)
                for task in tasks
            ]
        )

        tasks = []

        for task_result in result:
            # Continue if task has succeeded
            if task_result.success:
                continue

            # Do not retry task if it's failed with non retry status
            if task_result.status not in task_result.task.retry_status:
                continue

            # Stop after task failed more than max_fails
            if task_result.task.max_fails is not None:
                if task_result.task.fails > task_result.task.max_fails:
                    message = "Task max_fails reached"

                    if task_result.endpoint is not None:
                        message += f" ({task_result.endpoint})"

                    logger.error(message)

                    continue

            tasks.append(task_result.task)

        step += 1

        if len(tasks) > 0:
            logger.debug(f"Retrying {len(tasks)} tasks after {step} steps")
