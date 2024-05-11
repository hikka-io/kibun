from kibun.backend.aio.response import process_response
from aiosocks.connector import ProxyClientRequest
from aiosocks.connector import ProxyConnector
from kibun import constants
import aiohttp
import asyncio


def get_session_aio(proxy_type: str, timeout: int = 10):
    if proxy_type == constants.PROXY_TYPE_HTTP:
        return aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=timeout)
        )

    if proxy_type == constants.PROXY_TYPE_TOR:
        return aiohttp.ClientSession(
            connector=ProxyConnector(remote_resolve=False),
            timeout=aiohttp.ClientTimeout(total=timeout),
            request_class=ProxyClientRequest,
        )

    return None


async def make_request_aio(
    session,
    url,
    headers=None,
    cookies=None,
    method="GET",
    params={},
    proxy=None,
    error_markers=[],
):
    try:
        headers = (
            headers
            if headers
            else {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; rv:91.0) Gecko/20100101 Firefox/91.0"
            }
        )

        if method == "GET":
            async with session.get(
                url,
                headers=headers,
                cookies=cookies,
                proxy=proxy,
                ssl=False,
            ) as r:
                return await process_response(r, error_markers)

        if method == "POST":
            async with session.post(
                url,
                headers=headers,
                cookies=cookies,
                proxy=proxy,
                ssl=False,
                json=params,
            ) as r:
                return await process_response(r, error_markers)

    except (aiohttp.ClientError, asyncio.exceptions.TimeoutError):
        return None, constants.NETWORK_ERROR
