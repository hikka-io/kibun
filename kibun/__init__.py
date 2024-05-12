from kibun.logger import logger
import asyncio
import random


async def kibun_loop(tasks, semaphore_number=1):
    semaphore = asyncio.Semaphore(semaphore_number)
    step = 0

    logger.info(f"Got {len(tasks)} tasks")

    while len(tasks) > 0:
        logger.debug(f"Steps done: {step}")

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

            # Stop after task failed more than max_fails
            if task_result.task.max_fails is not None:
                if task_result.task.fails > task_result.task.max_fails:
                    logger.error("Task max_fails reached")
                    continue

            tasks.append(task_result.task)

        if len(tasks) > 0:
            logger.debug(f"Retrying {len(tasks)} tasks")

        step += 1
