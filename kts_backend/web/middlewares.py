import base64
import json
import typing

from aiohttp.web_exceptions import HTTPException, HTTPUnprocessableEntity
from aiohttp.web_middlewares import middleware
from aiohttp_apispec import validation_middleware
from aiohttp_session import get_session, session_middleware
from aiohttp_session.cookie_storage import EncryptedCookieStorage
from cryptography.fernet import Fernet
from sqlalchemy.exc import IntegrityError
from kts_backend.users.admin.models import Admin
from kts_backend.web.utils import error_json_response

if typing.TYPE_CHECKING:
    from kts_backend.web.app import Application, Request


@middleware
async def auth_middleware(request: "Request", handler: callable):
    session = await get_session(request)
    if session:
        request.admin = Admin.from_session(session)
    return await handler(request)


HTTP_ERROR_CODES = {
    400: "bad_request",
    401: "unauthorized",
    403: "forbidden",
    404: "not_found",
    405: "not_implemented",
    409: "conflict",
    500: "internal_server_error",
}


@middleware
async def error_handling_middleware(request: "Request", handler):
    try:
        response = await handler(request)
        return response
    except HTTPUnprocessableEntity as e:
        return error_json_response(
            http_status=400,
            status="bad_request",
            message=e.reason,
            data=json.loads(e.text),
        )
    except IntegrityError as e:
        correct_status = 500
        if e.orig.pgcode == "23505":
            correct_status = 409
        if e.orig.pgcode == "23502":
            correct_status = 400
        if e.orig.pgcode == "23503":
            correct_status = 404
        return error_json_response(
            http_status=correct_status,
            status=HTTP_ERROR_CODES[correct_status],
            message=str(e),
        )
    except HTTPException as e:
        return error_json_response(
            http_status=e.status,
            status=HTTP_ERROR_CODES[e.status],
            message=str(e),
        )
    except Exception as e:
        request.app.logger.error("Exception", exc_info=e)
        return error_json_response(
            http_status=500, status="internal server error", message=str(e)
        )


def setup_middlewares(app: "Application"):
    app.config.session.key = base64.urlsafe_b64decode(Fernet.generate_key())

    app.middlewares.append(error_handling_middleware)
    app.middlewares.append(validation_middleware)
    app.middlewares.append(
        session_middleware(EncryptedCookieStorage(app.config.session.key))
    )

    print("KEY KEY KEY", app.config.session.key)
    app.middlewares.append(auth_middleware)
