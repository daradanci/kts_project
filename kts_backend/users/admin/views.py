from aiohttp.web import HTTPForbidden, HTTPUnauthorized
from aiohttp_apispec import request_schema, response_schema
from aiohttp_session import new_session

from app.admin.schemes import AdminSchema
from app.web.app import View
from app.web.utils import json_response
import ast
import base64
import json
import uuid

from aiohttp.web_exceptions import HTTPForbidden, HTTPUnauthorized
from aiohttp_apispec import request_schema, response_schema, docs
from aiohttp_session import new_session, get_session

from app.admin.models import Admin
from app.admin.schemes import AdminLoginSchema, AdminLoginResponseSchema
from app.web.app import View
# from aiohttp.web_response import json_response
from app.web.utils import json_response
from hashlib import sha256

from app.web.schemes import OkResponseSchema
from app.store.admin.accessor import AdminAccessor
from app.web.mixins import AuthRequiredMixin


class AdminLoginView(View):
    @docs(tags=["web"], summary="Admin login", description="Admin login")
    @request_schema(AdminLoginSchema)
    @response_schema(OkResponseSchema)
    async def post(self):
        # data = self.request["data"]

        data = self.data
        _admin = await self.store.admins.get_by_email(email=data['email'])
        if _admin is None:
            raise HTTPForbidden(reason='No admin with requested email')

        print('REQUEST.PASSWORD:', data['password'])
        print('EXISTING_PASSWORD:', sha256(_admin.password.encode()).hexdigest())
        # if 'password' in data and data['password'] == base64.b64decode(_admin.password).decode('ascii'):
        if 'password' in data and  _admin.password==sha256(data['password'].encode()).hexdigest():
            session = await new_session(request=self.request)
            session['admin'] = json.dumps({"id": _admin.id, "email": _admin.email})
            print('LOGGED SUCCESSFULLY')
            print(session['admin'])
            return json_response(
                data={
                    # AdminLoginResponseSchema().dump(_admin)
                    #
                    "id": _admin.id,
                    "email": _admin.email,

                })
        raise HTTPForbidden


class AdminCurrentView(AuthRequiredMixin, View):
    @docs(tags=["web"], summary="Current admin", description="Current admin")
    @response_schema(OkResponseSchema)
    async def get(self):
        _admin = self.request.admin
        return json_response(data={
            "id": _admin.id,
            "email": _admin.email

        })
