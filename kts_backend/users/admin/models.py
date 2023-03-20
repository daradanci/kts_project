import ast
from dataclasses import dataclass
from hashlib import sha256
from typing import Optional

from kts_backend.store.database.sqlalchemy_base import db
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean


@dataclass
class Admin:
    id: int
    email: str
    password: Optional[str] = None

    def is_password_valid(self, password: str):
        return self.password == sha256(password.encode()).hexdigest()

    @classmethod
    def from_session(cls, session: Optional[dict]) -> Optional["Admin"]:
        session_admin = ast.literal_eval(session["admin"])
        return cls(id=session_admin["id"], email=session_admin["email"])
        # return cls(id=session["admin"]["id"], email=session["admin"]["email"])


class AdminModel(db):
    __tablename__ = "admins"
    id = Column(Integer, primary_key=True, index=True, unique=True)
    email = Column(String, unique=True, nullable=False)
    password = Column(String)
