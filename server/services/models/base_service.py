from abc import ABCMeta
from .singleton import SingletonMeta


class BaseService(ABCMeta, SingletonMeta):
    pass
