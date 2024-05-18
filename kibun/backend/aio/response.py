from kibun import constants


async def process_response(r, error_markers):
    if not (content := await r.content.read()):
        return None, constants.CONTENT_ERROR

    # Special case for html based text errors
    try:
        decoded = content.decode("utf-8")

        # Handle custom errors
        for error in error_markers:
            if error["marker"] in decoded:
                return None, error["status"]

    except:  # noqa: E722
        pass

    if r.status == 404:
        return content, constants.NOT_FOUND_ERROR

    if r.status == 403:
        return None, constants.FORBIDDEN_ERROR

    if r.status != 200:
        return None, constants.REQUEST_ERROR

    return content, None
