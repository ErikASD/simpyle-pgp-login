from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, exists
from sqlalchemy.orm import relationship
from database import Base
import time
from uuid import uuid4
from hashlib import sha256
import random

def get_uuid():
    return str(uuid4())

def get_current_time():
    return int(time.time())


class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, default=get_uuid)
    display = Column(String, unique=True, index=True)
    public_fingerprint = Column(String, unique=True, index=True)
    login_codes = relationship("LoginCode", back_populates="user", order_by='LoginCode.time_created.asc()')
    time_created = Column(Integer, default=get_current_time)

    def create(db, display, public_fingerprint, login_code):
        db_user = User.get_by_public_fingerprint(db, public_fingerprint)
        if db_user: #protects against unlikely edge cases
            return db_user

        while User.exists(db, display):
            display += str(random.randint(0, 9))

        db_user = User(
            display = display,
            public_fingerprint = public_fingerprint,
        )
        db.add(db_user)
        login_code.user = db_user
        db.commit()
        db.refresh(db_user)
        return db_user

    def login(login_code):
        return login_code.user

    def exists(db, display):
        exist = db.scalar(exists().where(User.display == display).select())
        return exist

    def get(db, id):
        user = db.query(User).filter(User.id == id).one_or_none()
        return user

    def get_by_display(db, display):
        user = db.query(User).filter(User.display == display).one_or_none()
        return user

    def get_by_public_fingerprint(db, public_fingerprint):
        user = db.query(User).filter(User.public_fingerprint == public_fingerprint).one_or_none()
        return user

class LoginCode(Base):
    __tablename__ = "login_codes"

    id = Column(String, primary_key=True, default=get_uuid)
    public_fingerprint = Column(String, index=True)
    code = Column(String, index=True)
    user_id = Column(String, ForeignKey("users.id"))
    user = relationship("User", back_populates="login_codes")
    time_created = Column(Integer, default=get_current_time)

    def create(db, public_fingerprint, code):
        db_user = User.get_by_public_fingerprint(db, public_fingerprint)
        user_id = db_user.id if db_user else None
        db_login_code = LoginCode(
            public_fingerprint = public_fingerprint,
            user_id = user_id,
            code = code,
        )
        db.add(db_login_code)
        db.commit()
        db.refresh(db_login_code)
        return db_login_code

    def get(db, public_fingerprint, code):
        db_login_code = db.query(LoginCode).filter(LoginCode.public_fingerprint == public_fingerprint, LoginCode.code == code).order_by(LoginCode.time_created.desc()).one_or_none()
        return db_login_code

    def delete_expired(db, expire_time):
        query = LoginCode.__table__.delete().where(LoginCode.time_created < int(time.time()) - expire_time)
        db.execute(query)
        db.commit()
