# 项目：数据库
# 模块：mongoengine bug fix
# 作者：黄涛
# License:GPL
# Email:huangtao.sh@icloud.com
# 创建：2016-08-29 20:02

import mongoengine
import pymongo
from mongoengine import signals

def _iter_results(self):
    """A generator for iterating over the result cache.

    Also populates the cache if there are more possible results to yield.
    Raises StopIteration when there are no more results"""
    #if self._result_cache is None:
    #    self._result_cache = []   这两行代码纯粹无用
    if self._result_cache:
        yield from self._result_cache
    while self._has_more:
        self._populate_cache()
        yield from self._result_cache

    '''以下这段代码写的真是无语，上面三句话可以搞定的事情
    pos = 0
    while True:
        upper = len(self._result_cache)
        while pos < upper:
            yield self._result_cache[pos]
            pos += 1
        if not self._has_more:
            #raise StopIteration
            return   # generator should return None rather a StopIteration
        if len(self._result_cache) <= pos:
            self._populate_cache()

DeprecationWarning: save is deprecated. Use insert_one or replace_one instead

'''

def save(self, force_insert=False, validate=True, clean=True,
         write_concern=None, cascade=None, cascade_kwargs=None,
         _refs=None, save_condition=None, **kwargs):
    """Save the :class:`~mongoengine.Document` to the database. If the
    document already exists, it will be updated, otherwise it will be
    created.

    :param force_insert: only try to create a new document, don't allow
        updates of existing documents
    :param validate: validates the document; set to ``False`` to skip.
    :param clean: call the document clean method, requires `validate` to be
        True.
    :param write_concern: Extra keyword arguments are passed down to
        :meth:`~pymongo.collection.Collection.save` OR
        :meth:`~pymongo.collection.Collection.insert`
        which will be used as options for the resultant
        ``getLastError`` command.  For example,
        ``save(..., write_concern={w: 2, fsync: True}, ...)`` will
        wait until at least two servers have recorded the write and
        will force an fsync on the primary server.
    :param cascade: Sets the flag for cascading saves.  You can set a
        default by setting "cascade" in the document __meta__
    :param cascade_kwargs: (optional) kwargs dictionary to be passed throw
        to cascading saves.  Implies ``cascade=True``.
    :param _refs: A list of processed references used in cascading saves
    :param save_condition: only perform save if matching record in db
        satisfies condition(s) (e.g. version number).
        Raises :class:`OperationError` if the conditions are not satisfied

    .. versionchanged:: 0.5
        In existing documents it only saves changed fields using
        set / unset.  Saves are cascaded and any
        :class:`~bson.dbref.DBRef` objects that have changes are
        saved as well.
    .. versionchanged:: 0.6
        Added cascading saves
    .. versionchanged:: 0.8
        Cascade saves are optional and default to False.  If you want
        fine grain control then you can turn off using document
        meta['cascade'] = True.  Also you can pass different kwargs to
        the cascade save using cascade_kwargs which overwrites the
        existing kwargs with custom values.
    .. versionchanged:: 0.8.5
        Optional save_condition that only overwrites existing documents
        if the condition is satisfied in the current db record.
    .. versionchanged:: 0.10
        :class:`OperationError` exception raised if save_condition fails.
    .. versionchanged:: 0.10.1
        :class: save_condition failure now raises a `SaveConditionError`
    """
    signals.pre_save.send(self.__class__, document=self)

    if validate:
        self.validate(clean=clean)

    if write_concern is None:
        write_concern = {"w": 1}

    doc = self.to_mongo()

    created = ('_id' not in doc or self._created or force_insert)

    signals.pre_save_post_validation.send(self.__class__, document=self,
                                          created=created)

    try:
        collection = self._get_collection()
        if self._meta.get('auto_create_index', True):
            self.ensure_indexes()
        if created:
            if force_insert:
                #object_id = collection.insert(doc, **write_concern)
                collection.insert_one(doc) #replace to this 
            else:
                # object_id = collection.save(doc, **write_concern)
                collection.insert_one(doc)
                # In PyMongo 3.0, the save() call calls internally the _update() call
                # but they forget to return the _id value passed back, therefore getting it back here
                # Correct behaviour in 2.X and in 3.0.1+ versions
                '''The following code is not needed.
                if not object_id and pymongo.version_tuple == (3, 0):
                    pk_as_mongo_obj = self._fields.get(self._meta['id_field']).to_mongo(self.pk)
                    object_id = self._qs.filter(pk=pk_as_mongo_obj).first() and \
                                self._qs.filter(pk=pk_as_mongo_obj).first().pk
                '''
            object_id=doc['_id']
        else:
            object_id = doc['_id']
            updates, removals = self._delta()
            # Need to add shard key to query, or you get an error
            if save_condition is not None:
                select_dict = transform.query(self.__class__,
                                              **save_condition)
            else:
                select_dict = {}
            select_dict['_id'] = object_id
            shard_key = self.__class__._meta.get('shard_key', tuple())
            for k in shard_key:
                path = self._lookup_field(k.split('.'))
                actual_key = [p.db_field for p in path]
                val = doc
                for ak in actual_key:
                    val = val[ak]
                select_dict['.'.join(actual_key)] = val

            def is_new_object(last_error):
                if last_error is not None:
                    updated = last_error.get("updatedExisting")
                    if updated is not None:
                        return not updated
                return created

            update_query = {}

            if updates:
                update_query["$set"] = updates
            if removals:
                update_query["$unset"] = removals
            if updates or removals:
                upsert = save_condition is None
                #collection.replace_one(select_dict,update_query,
                #                       upsert=upsert)
                last_error = collection.update_one(select_dict, update_query,
                                               upsert=upsert)
                '''
                if not upsert and last_error["n"] == 0:
                    raise SaveConditionError('Race condition preventing'
                                             ' document update detected')
                created = is_new_object(last_error)
                '''

        if cascade is None:
            cascade = self._meta.get(
                'cascade', False) or cascade_kwargs is not None

        if cascade:
            kwargs = {
                "force_insert": force_insert,
                "validate": validate,
                "write_concern": write_concern,
                "cascade": cascade
            }
            if cascade_kwargs:  # Allow granular control over cascades
                kwargs.update(cascade_kwargs)
            kwargs['_refs'] = _refs
            self.cascade_save(**kwargs)
    except pymongo.errors.DuplicateKeyError as err:
        message = 'Tried to save duplicate unique keys (%s)'
        raise NotUniqueError(message % str(err))
    except pymongo.errors.OperationFailure as err:
        message = 'Could not save document (%s)'
        if re.match('^E1100[01] duplicate key', str(err)):
            # E11000 - duplicate key error index
            # E11001 - duplicate key on update
            message = 'Tried to save duplicate unique keys (%s)'
            raise NotUniqueError(message % str(err))
        raise OperationError(message % str(err))
    id_field = self._meta['id_field']
    if created or id_field not in self._meta.get('shard_key', []):
        self[id_field] = self._fields[id_field].to_python(object_id)

    signals.post_save.send(self.__class__, document=self, created=created)
    self._clear_changed_fields()
    self._created = False
    return self

mongoengine.queryset.QuerySet._iter_results=_iter_results
mongoengine.document.Document.save=save
