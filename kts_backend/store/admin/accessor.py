import base64
import typing
from hashlib import sha256
from typing import Optional
from cryptography.fernet import Fernet
from app.store.database.database import Database

from app.base.base_accessor import BaseAccessor
from app.admin.models import Admin, AdminModel
from sqlalchemy import select, text, exc, delete, insert

if typing.TYPE_CHECKING:
    from app.web.app import Application


class AdminAccessor(BaseAccessor):
    async def connect(self, app: "Application"):
        self.app = app
        _admin=await self.get_by_email(app.config.admin.email)
        if _admin is None:
            _admin=await self.create_admin(email=app.config.admin.email,password=app.config.admin.password)
        return None

    async def get_by_email(self, email: str) -> Optional[Admin]:
        async with self.app.database.session() as session:
            result_raw = await session.execute(select(AdminModel).filter_by(email=email))
            result = [res._mapping['AdminModel'] for res in result_raw]
            return result[0] if len(result) > 0 else None

    async def create_admin(self, email: str, password: str) -> Admin:
        async with self.app.database.session() as session:
            # new_admin = AdminModel(email=email, password=base64.b64encode(password.encode('ascii')).decode('ascii'))

            new_admin = AdminModel(email=email, password=sha256(password.encode()).hexdigest())

            session.add(new_admin)
            await session.commit()
            # return new_admin
            return Admin(id=new_admin.id, email=new_admin.email)

