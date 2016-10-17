#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from __future__ import unicode_literals

from grako.model import NodeWalker

from b3j0f.requester.request.expr import Expression as E, Function as F
from b3j0f.requester.request.consts import FuncName
from b3j0f.requester.request.crud.create import Create
from b3j0f.requester.request.crud.read import Read
from b3j0f.requester.request.crud.update import Update
from b3j0f.requester.request.crud.delete import Delete


class Walker(NodeWalker):
    def walk_forward_value(self, node):
        return self.walk(node.value)

    def walk_digits(self, node):
        return int(node.value)

    def walk_sign(self, node):
        """
        Convert sign to a positive or negative factor
        """
        if node.value == '-':
            return -1

        else:
            return 1

    def walk_characters(self, node):
        return node.value

    def walk_integer(self, node):
        sign = 1 if node.sign is None else self.walk(node.sign)
        value = self.walk(node.value)

        return sign * value

    def walk_floating(self, node):
        sign = 1 if node.sign is None else self.walk(node.sign)
        intpart = self.walk(node.intpart)
        floatpart = self.walk(node.floatpart)

        floating = sign * (intpart + 0.1 * floatpart)
        return floating

    def walk_true(self, node):
        return True

    def walk_false(self, node):
        return False

    def walk_none(self, node):
        return None

    def walk_name(self, node):
        return node.value

    def walk_expression(self, node):
        e = E(self.walk(node.name))

        alias = self.walk(node.as_)
        if alias:
            e = e.as_(alias)

        return e

    def walk_function(self, node):
        args = [self.walk(arg) for arg in node.args]
        f = F(self.walk(node.f), params=args)

        alias = self.walk(node.as_)
        if alias:
            f = f.as_(alias)

        return f

    def walk_condop(self, node):
        return getattr(FuncName, node.value, node.value)

    def walk_condition(self, node):
        cond = self.walk(node.left)

        if node.condop is not None:
            condop = self.walk(node.condop)
            right = self.walk(node.right)

            cond = F(condop, params=[cond, right])

        return cond

    def walk_kv(self, node):
        return self.walk(node.key), self.walk(node.value)

    def walk_kvs(self, node):
        return {k: v for (k, v) in [self.walk(kv) for kv in node.kvs]}

    def walk_sorter(self, node):
        mod = 'DESC' if node.sortmod == 'DESC' else 'ASC'
        name = self.walk(node.name)

        return name, mod

    def walk_orderby(self, node):
        return [self.walk(order) for order in node.values_]

    def walk_with(self, node):
        return self.walk(node.dparams)

    def walk_create(self, node):
        kwargs = {
            'values': self.walk(node.fields),
            'name': self.walk(node.name) or '',
            'dparams': self.walk(node.with_),
        }

        return Create(**kwargs)

    def walk_all_(self, node):
        print('hey')
        return ''

    def walk_read(self, node):
        if node.names:
            select = [self.walk(name) for name in node.names]
        else:
            select = self.walk(node.all)

        kwargs = {
            'select': select,
            'limit': self.walk(node.limit),
            'dparams': self.walk(node.with_),
        }

        read = Read(**kwargs)

        where = self.walk(node.where)
        if where:
            read = read.where(where)

        groupby = self.walk(node.groupby)
        if groupby:
            read = read.groupby(groupby)

        orderby = self.walk(node.orderby)
        if orderby:
            read = read.orderby(orderby)

        return read

    def walk_update(self, node):
        kwargs = {
            'values': self.walk(node.fields),
            'name': self.walk(node.name) or '',
            'dparams': self.walk(node.with_),
        }

        update = Update(**kwargs)

        where = self.walk(node.where)
        if where:
            update = update.where(where)

        return update

    def walk_delete(self, node):
        kwargs = {
            'names': [self.walk(name) for name in node.names],
            'dparams': self.walk(node.with_),
        }

        delete = Delete(**kwargs)

        where = self.walk(node.where)
        if where:
            delete = delete.where(where)

        return delete

    def walk_crud(self, node):
        crud = self.walk(node.crudop)

        alias = self.walk(node.as_)
        if alias:
            crud = crud.as_(alias)

        return crud

    def walk_AST(self, node):
        return self.walk(node.request)
