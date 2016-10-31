# Copyright 2014-2016 Morgan Delahaye-Prat. All Rights Reserved.
#
# Licensed under the Simplified BSD License (the "License");
# you may not use this file except in compliance with the License.
"""Implements a RESTful provider for CRUD operations."""


import asyncio

from hypr.globals import request
from hypr.web_exceptions import abort
from hypr.providers.base import Provider
from hypr.helpers.mini_dsl import parse_clause
from collections import defaultdict


class _Query:

    def __init__(self, filters, limit, offset):
        self.filters = filters
        self.limit = limit
        self.offset = offset


class CRUDProvider(Provider):
    """RESTful CRUD provider.

    The provider implements all the required methods to perform CRUD operations
    on the model associated with it through the HTTP protocol. It should
    perform nicely with most of the use-cases but non-trivial models may
    require additional development.

    The following features are provided out of the box :

    - searching, filtering and pagination on GET requests with transparent
      support for range filtering and dates.
    - bulk operations on POST, PUT/PATCH and DELETE.
    - atomicity of each request is guaranteed for transactional backends.

    Attributes:
        __model__: A Model associated with the current provider.
    """

    __model__ = None

    def url_to_uid(self, **kwargs):
        """Convert the URL arguments to a unique resource identifier.

        The unique identifier (uid) of a resource is a set of values unique to
        each instance of a model. The default implementation of url_to_uid()
        maps each URL arguments to an element of the model's key otherwise a
        custom implementation must be done.

        Returns: a tuple.

        Raises:
            NotImplementedError: custom implementation required.
        """
        key = self.__model__._key()
        rv = tuple(kwargs.get(cut) for cut in key if cut in kwargs)

        # check if the URL, mapping and uid match
        if len(kwargs) != len(key) or len(kwargs) != len(rv):
            err_msg = '%s : custom url_to_uid() is required'
            raise NotImplementedError(err_msg % self.__class__.__name__)

        return rv

    def parse_query(self, args=None):
        """Parse the query string of the request."""
        app = request.app

        # for overloading purpose
        if args is None:    # pragma: no cover
            args = request.args

        # ensure offset is a positive integer
        offset = args.get('_offset', '0')
        if not offset.isdigit():
            abort(400)

        # ensure limit is a positive integer
        limit = args.get('_limit', '0')
        if not limit.isdigit():
            abort(400)

        limit = int(limit) or app.config.get('CRUD_DEFAULT_LIMIT', 0)
        absolute = app.config.get('CRUD_ABSOLUTE_LIMIT', limit)

        # get the filters
        filters = defaultdict(tuple)
        for group, (key, value) in enumerate(args.items()):
            if key.startswith('_'):
                continue
            filters[key] += parse_clause(value, group)

        return _Query(
            filters=dict(filters),
            limit=min(limit, absolute),
            offset=max(int(offset), 0)
        )

    @asyncio.coroutine
    def get(self, **kwargs):
        """Get a specific resource or a collection of resources."""
        model = self.__model__

        # get a specific resource.
        if len(kwargs):
            return model.one(*self.url_to_uid(**kwargs)) or abort(404)

        query = self.parse_query()

        # build the collection response object
        rv = None   # failsafe
        try:
            rv = {
                'count': model.count(**query.filters),
                'content': model.get(_limit=query.limit,
                                     _offset=query.offset,
                                     **query.filters)
            }
        except:
            abort(400)

        return rv

    @asyncio.coroutine
    def post(self, _data=None, _bulk=None, _commit=True):
        """Create a new resource."""
        model = self.__model__

        # get the _data from the request if None is given as method args.
        if _data is None:
            _data = yield from request.json()
        if _data is None:
            abort(400)

        # determine if this is a bulk insert or not.
        if _bulk is None:
            _bulk = request.args.get('_bulk', '').lower() in ['true', '1']

        # bulk insertion is based on the basic insertion
        if _bulk:
            content = []
            for resource in _data:
                rv, _ = yield from self.post(
                    _data=resource, _bulk=False, _commit=False)
                content.append(rv)

            rv = {
                'content': content,
                'count': len(content)
            }

        # create one resource
        # TODO: validation
        else:
            try:
                rv = model(**_data)
            except TypeError:
                model.rollback()
                abort(400)

            rv.save(commit=False)   # mark the resource for persistence

        # commit data
        # TODO: handle commit failure
        if _commit:
            model.commit()

        return rv, 201

    def patch(self, _data=None, _bulk=None, **kwargs):
        """The patch() method is an alias to put()."""
        return self.put(_data=_data, _bulk=_bulk, **kwargs)

    @asyncio.coroutine
    def put(self, _data=None, _bulk=None, _commit=True, **kwargs):
        """Update an existing resource."""
        model = self.__model__

        # get the _data from the request if None is given as method args.
        if _data is None:
            _data = yield from request.json()
        if _data is None:
            abort(400)

        # determine if this is a bulk insert or not.
        if _bulk is None:
            _bulk = request.args.get('_bulk', '').lower() in ['true', '1']

        if _bulk and not kwargs:
            content = []
            key = model._key()
            for resource in _data:
                url_args = {k: v for k, v in resource.items() if k in key}
                if len(url_args) != len(key):
                    model.rollback()
                    abort(400)
                rv = yield from self.put(
                    _data=resource, _bulk=False, _commit=False, **url_args)
                content.append(rv)

            rv = {
                'content': content,
                'count': len(content)
            }

        # update a resource
        elif not _bulk and kwargs:
            rv = model.one(*self.url_to_uid(**kwargs))  # retrieve the resource
            if rv is None and not _commit:
                model.rollback()
                abort(400)
            elif rv is None:
                model.rollback()
                abort(404)  # otherwise, 404 NOT FOUND

            # update the resource attributes
            for k, v in _data.items():
                if hasattr(rv, k):
                    if getattr(rv, k) != v:
                        setattr(rv, k, v)
                else:
                    model.rollback()
                    abort(400)

            rv.save(commit=False)

        # invalid request
        else:
            abort(400)

        # commit data
        # TODO: handle commit failure
        if _commit:
            model.commit()

        return rv

    @asyncio.coroutine
    def delete(self, _data=None, _bulk=None, _commit=True, **kwargs):
        """Delete an existing resource."""
        model = self.__model__

        # determine if this is a bulk insert or not.
        if _bulk is None:
            _bulk = request.args.get('_bulk', '').lower() in ['true', '1']

        # bulk delete
        if _bulk and not kwargs:

            # get the _data from the request if None is given as method args.
            if _data is None:
                _data = yield from request.json()
            if _data is None:
                abort(400)

            content = []
            key = model._key()
            for resource in _data:
                url_args = {k: v for k, v in resource.items() if k in key}
                if len(url_args) != len(key):
                    model.rollback()
                    abort(400)
                rv = yield from self.delete(
                    _bulk=False, _commit=False, **url_args)
                content.append(rv)

        # delete a resource
        elif not _bulk and kwargs:
            rv = model.one(*self.url_to_uid(**kwargs))  # retrieve the resource
            # if commit is not active, rollback all the transaction on failure
            if rv is None and not _commit:
                model.rollback()
                abort(400)
            elif rv is None:
                abort(404)  # otherwise, 404 NOT FOUND

            rv.delete(commit=False)

        # invalid request
        else:
            abort(400)

        # commit data
        # TODO: handle commit failure
        if _commit:
            model.commit()
            return '', 204

        return rv
