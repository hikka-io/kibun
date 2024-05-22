from urllib.parse import urlparse
from kibun.logger import logger
import aiofiles
import os


async def save_text_to_file(path, text):
    # print(f"Saved path {path}")

    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)

        async with aiofiles.open(path, "w") as file:
            await file.write(text)

        return True

    except Exception as _:
        logger.error(f"Saving text to file {path} has failed")
        return False


def get_website_address(url):
    return urlparse(url).netloc
