from dataclasses import dataclass
from kibun import constants


@dataclass
class Task:
    method: str
    allowed_status: list
    delete_status: list
    retry_status: list
    done_status: list
    endpoint: callable
    executor: callable
    process: callable
    parser: callable
    delete: callable
    fails: int
    sleep: int
    params: dict
    save_path: str | None
    response_format: str
    proxy: str | None
    proxy_type: str
    proxy_timeout: int
    max_attempts: int
    endpoint_kwargs: dict
    process_kwargs: dict
    parser_kwargs: dict
    executor_kwargs: dict
    delete_kwargs: dict
    max_fails: int | None
    error_markers: list
    headers: dict | None


@dataclass
class TaskResult:
    task: Task
    success: bool
    endpoint: str | None
    status: str | None


def create_task(
    executor,
    endpoint,
    parser=None,
    process=None,
    delete=None,
    allowed_status=[],
    delete_status=[],
    retry_status=[],
    done_status=[],
    sleep=0,
    fails=0,
    save_path=None,
    params={},
    method="GET",
    response_format=constants.RESPONSE_HTML,
    proxy=None,
    proxy_type=constants.PROXY_TYPE_HTTP,
    proxy_timeout=10,
    max_attempts=1,
    endpoint_kwargs={},
    process_kwargs={},
    parser_kwargs={},
    executor_kwargs={},
    delete_kwargs={},
    max_fails=10,
    error_markers=constants.DEFAULT_MARKERS,
    headers=None,
):
    return Task(
        method,
        allowed_status,
        delete_status,
        retry_status,
        done_status,
        endpoint,
        executor,
        process,
        parser,
        delete,
        fails,
        sleep,
        params,
        save_path,
        response_format,
        proxy,
        proxy_type,
        proxy_timeout,
        max_attempts,
        endpoint_kwargs,
        process_kwargs,
        parser_kwargs,
        executor_kwargs,
        delete_kwargs,
        max_fails,
        error_markers,
        headers,
    )


def create_task_result(task, success, endpoint=None, status=None):
    return TaskResult(task, success, endpoint, status)
