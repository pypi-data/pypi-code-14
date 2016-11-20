# coding=utf-8

from .client import ZhihuClient
from .exception import (
    ZhihuException, ZhihuWarning,
    NeedCaptchaException, UnexpectedResponseException, GetDataErrorException
)
from .helpers import shield, SHIELD_ACTION
from .zhcls import (
    Activity, ActType, Answer, Article, Comment, Column, Collection, People,
    Question, Topic, ANONYMOUS
)

__all__ = ['ZhihuClient', 'ANONYMOUS', 'Activity', 'ActType', 'Article',
           'Answer', 'Collection', 'Column', 'Comment', 'People', 'Question',
           'Topic', 'ZhihuException', 'ZhihuWarning', 'NeedCaptchaException',
           'UnexpectedResponseException', 'GetDataErrorException',
           'SHIELD_ACTION', 'shield']

__version__ = '0.0.23'
