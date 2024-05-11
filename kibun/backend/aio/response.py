from kibun import constants


async def process_response(r):
    if not (content := await r.content.read()):
        return None, constants.CONTENT_ERROR

    if r.status == 404:
        return content, constants.NOT_FOUND_ERROR

    if r.status == 403:
        return None, constants.FORBIDDEN_ERROR

    if r.status != 200:
        return None, constants.REQUEST_ERROR

    # Special case for html based text errors
    try:
        decoded = content.decode("utf-8")

        if constants.MARKER_CLOUDFLARE_CHALLENGE in decoded:
            return None, constants.CLOUDFLARE_ERROR

        if constants.MARKER_PROXY_ERROR in decoded:
            return None, constants.REQUEST_ERROR

    except:  # noqa: E722
        pass

    return content, None
