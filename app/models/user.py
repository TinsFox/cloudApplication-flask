"""
    Created by TinsFox on 2020-02-19.
"""

__author__ = 'TinsFox'

from lin.core import User as _User
from sqlalchemy import Column, String


class User(_User):
    # 扩展user，增加一个phone属性
    openid = Column(String(30), unique=True)
