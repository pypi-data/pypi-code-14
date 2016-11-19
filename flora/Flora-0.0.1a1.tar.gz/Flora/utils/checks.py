from . import Config
from .utils import has_permissions
from datetime import datetime


def reload(*args, **kwargs):
    Config.reload()

def IsOwner(ctx):
    return ctx.message.author.id == Config.OwnerID

def ServerOwner(ctx):
    return is_owner(ctx) or (ctx.message.author == ctx.message.server.owner)

def SelfBot(*args, **kwargs):
    return Config.SelfBot

def NoSelfBot(*args, **kwargs):
    return not Config.SelfBot

def NotBlacklisted(ctx):
    return not ctx.message.autor.id in C['Blacklist']

def HasPermissionsOr(ctx, **kwargs):
    if IsOwner(ctx):
        return True
    P = ctx.message.author.permissions_in(ctx.message.channel)
    return has_permissions(P, **kwargs)
