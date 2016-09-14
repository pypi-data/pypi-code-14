from __future__ import division
import collections
from collections import OrderedDict
import copy
from datetime import datetime
import functools
import itertools
import json
from operator import itemgetter
import threading
import time
import warnings

try:
    from bson import json_util, SON
except ImportError:
    json_utils = SON = None
try:
    import execjs
except ImportError:
    execjs = None

try:
    from pymongo import ReturnDocument
except ImportError:
    class ReturnDocument(object):
        BEFORE = False
        AFTER = True

from sentinels import NOTHING
from six import iteritems
from six import iterkeys
from six import itervalues
from six import MAXSIZE
from six.moves import xrange
from six import string_types
from six import text_type


from mongomock.command_cursor import CommandCursor
from mongomock import DuplicateKeyError
from mongomock.filtering import filter_applies
from mongomock.filtering import iter_key_candidates
from mongomock import helpers
from mongomock import InvalidOperation
from mongomock import ObjectId
from mongomock import OperationFailure
from mongomock.results import DeleteResult
from mongomock.results import InsertManyResult
from mongomock.results import InsertOneResult
from mongomock.results import UpdateResult
from mongomock.write_concern import WriteConcern
from mongomock import WriteError

lock = threading.RLock()


def validate_is_mapping(option, value):
    if not isinstance(value, collections.Mapping):
        raise TypeError('%s must be an instance of dict, bson.son.SON, or '
                        'other type that inherits from '
                        'collections.Mapping' % (option,))


def validate_is_mutable_mapping(option, value):
    if not isinstance(value, collections.MutableMapping):
        raise TypeError('%s must be an instance of dict, bson.son.SON, or '
                        'other type that inherits from '
                        'collections.MutableMapping' % (option,))


def validate_ok_for_replace(replacement):
    validate_is_mapping('replacement', replacement)
    if replacement:
        first = next(iter(replacement))
        if first.startswith('$'):
            raise ValueError('replacement can not include $ operators')


def validate_ok_for_update(update):
    validate_is_mapping('update', update)
    if not update:
        raise ValueError('update only works with $ operators')
    first = next(iter(update))
    if not first.startswith('$'):
        raise ValueError('update only works with $ operators')


def validate_write_concern_params(**params):
    if params:
        WriteConcern(**params)


class BulkWriteOperation(object):
    def __init__(self, builder, selector, is_upsert=False):
        self.builder = builder
        self.selector = selector
        self.is_upsert = is_upsert

    def upsert(self):
        assert not self.is_upsert
        return BulkWriteOperation(self.builder, self.selector, is_upsert=True)

    def register_remove_op(self, multi):
        collection = self.builder.collection
        selector = self.selector

        def exec_remove():
            op_result = collection.remove(selector, multi=multi)
            if op_result.get("ok"):
                return {'nRemoved': op_result.get('n')}
            err = op_result.get("err")
            if err:
                return {"writeErrors": [err]}
            return {}
        self.builder.executors.append(exec_remove)

    def remove(self):
        assert not self.is_upsert
        self.register_remove_op(multi=True)

    def remove_one(self,):
        assert not self.is_upsert
        self.register_remove_op(multi=False)

    def register_update_op(self, document, multi, **extra_args):
        if not extra_args.get("remove"):
            validate_ok_for_update(document)

        collection = self.builder.collection
        selector = self.selector

        def exec_update():
            result = collection._update(spec=selector, document=document,
                                        multi=multi, upsert=self.is_upsert,
                                        **extra_args)
            ret_val = {}
            if result.get('upserted'):
                ret_val["upserted"] = result.get('upserted')
                ret_val["nUpserted"] = result.get('n')
            modified = result.get('nModified')
            if modified is not None:
                ret_val['nModified'] = modified
                ret_val['nMatched'] = modified
            if result.get('err'):
                ret_val['err'] = result.get('err')
            return ret_val
        self.builder.executors.append(exec_update)

    def update(self, document):
        self.register_update_op(document, multi=True)

    def update_one(self, document):
        self.register_update_op(document, multi=False)

    def replace_one(self, document):
        self.register_update_op(document, multi=False, remove=True)


class BulkOperationBuilder(object):
    def __init__(self, collection, ordered=False):
        self.collection = collection
        self.ordered = ordered
        self.results = {}
        self.executors = []
        self.done = False
        self._insert_returns_nModified = True
        self._update_returns_nModified = True

    def find(self, selector):
        return BulkWriteOperation(self, selector)

    def insert(self, doc):
        def exec_insert():
            self.collection.insert(doc)
            return {'nInserted': 1}
        self.executors.append(exec_insert)

    def __aggregate_operation_result(self, total_result, key, value):
        agg_val = total_result.get(key)
        assert agg_val is not None, "Unknow operation result %s=%s" \
                                    " (unrecognized key)" % (key, value)
        if isinstance(agg_val, int):
            total_result[key] += value
        elif isinstance(agg_val, list):
            if key == "upserted":
                new_element = {"index": len(agg_val), "_id": value}
                agg_val.append(new_element)
            else:
                agg_val.append(value)
        else:
            assert False, "Fixme: missed aggreation rule for type: %s for" \
                          " key {%s=%s}" % (type(agg_val), key, agg_val)

    def _set_nModified_policy(self, insert, update):
        self._insert_returns_nModified = insert
        self._update_returns_nModified = update

    def execute(self, write_concern=None):
        if not self.executors:
            raise InvalidOperation("Bulk operation empty!")
        if self.done:
            raise InvalidOperation("Bulk operation already executed!")
        self.done = True
        result = {'nModified': 0, 'nUpserted': 0, 'nMatched': 0,
                  'writeErrors': [], 'upserted': [], 'writeConcernErrors': [],
                  'nRemoved': 0, 'nInserted': 0}

        has_update = False
        has_insert = False
        broken_nModified_info = False
        for execute_func in self.executors:
            exec_name = execute_func.__name__
            op_result = execute_func()
            for (key, value) in op_result.items():
                self.__aggregate_operation_result(result, key, value)
            if exec_name == "exec_update":
                has_update = True
                if "nModified" not in op_result:
                    broken_nModified_info = True
            has_insert |= exec_name == "exec_insert"

        if broken_nModified_info:
            result.pop('nModified')
        elif has_insert and self._insert_returns_nModified:
            pass
        elif has_update and self._update_returns_nModified:
            pass
        elif self._update_returns_nModified and self._insert_returns_nModified:
            pass
        else:
            result.pop('nModified')
        return result


class Collection(object):

    def __init__(self, db, name):
        self.name = name
        self.full_name = "{0}.{1}".format(db.name, name)
        self._database = db
        self._documents = OrderedDict()
        self._uniques = []

    def __repr__(self):
        return "Collection({0}, '{1}')".format(self._database, self.name)

    def __getitem__(self, name):
        return self._database[self.name + '.' + name]

    def __getattr__(self, name):
        return self.__getitem__(name)

    def initialize_unordered_bulk_op(self):
        return BulkOperationBuilder(self, ordered=False)

    def initialize_ordered_bulk_op(self):
        return BulkOperationBuilder(self, ordered=True)

    def insert(self, data, manipulate=True, check_keys=True,
               continue_on_error=False, **kwargs):
        warnings.warn("insert is deprecated. Use insert_one or insert_many "
                      "instead.", DeprecationWarning, stacklevel=2)
        validate_write_concern_params(**kwargs)
        return self._insert(data)

    def insert_one(self, document):
        validate_is_mutable_mapping('document', document)
        return InsertOneResult(self._insert(document), acknowledged=True)

    def insert_many(self, documents, ordered=True):
        if not isinstance(documents, collections.Iterable) or not documents:
            raise TypeError('documents must be a non-empty list')
        for document in documents:
            validate_is_mutable_mapping('document', document)
        return InsertManyResult(self._insert(documents), acknowledged=True)

    def _insert(self, data):
        if isinstance(data, list):
            return [self._insert(item) for item in data]

        if not all(isinstance(k, string_types) for k in data):
            raise ValueError("Document keys must be strings")

        if '_id' not in data:
            data['_id'] = ObjectId()
        object_id = data['_id']
        if isinstance(object_id, dict):
            object_id = helpers.hashdict(object_id)
        if object_id in self._documents:
            raise DuplicateKeyError("Duplicate Key Error", 11000)
        for unique in self._uniques:
            find_kwargs = {}
            for key, direction in unique:
                if key in data:
                    find_kwargs[key] = data[key]
            answer = self.find(find_kwargs)
            if answer.count() > 0:
                raise DuplicateKeyError("Duplicate Key Error", 11000)
        with lock:
            self._documents[object_id] = self._internalize_dict(data)
        return data['_id']

    def _internalize_dict(self, d):
        return {k: copy.deepcopy(v) for k, v in iteritems(d)}

    def _has_key(self, doc, key):
        key_parts = key.split('.')
        sub_doc = doc
        for part in key_parts:
            if part not in sub_doc:
                return False
            sub_doc = sub_doc[part]
        return True

    def _remove_key(self, doc, key):
        key_parts = key.split('.')
        sub_doc = doc
        for part in key_parts[:-1]:
            sub_doc = sub_doc[part]
        del sub_doc[key_parts[-1]]

    def update_one(self, criteria, update, upsert=False):
        validate_ok_for_update(update)
        return UpdateResult(self._update(criteria, update, upsert=upsert),
                            acknowledged=True)

    def update_many(self, criteria, update, upsert=False):
        validate_ok_for_update(update)
        return UpdateResult(self._update(criteria, update, upsert=upsert,
                                         multi=True),
                            acknowledged=True)

    def replace_one(self, criteria, replacement, upsert=False):
        validate_ok_for_replace(replacement)
        return UpdateResult(self._update(criteria, replacement, upsert=upsert),
                            acknowledged=True)

    def update(self, spec, document, upsert=False, manipulate=False,
               multi=False, check_keys=False, **kwargs):
        warnings.warn("update is deprecated. Use replace_one, update_one or "
                      "update_many instead.", DeprecationWarning, stacklevel=2)
        return self._update(spec, document, upsert, manipulate, multi,
                            check_keys, **kwargs)

    def _update(self, spec, document, upsert=False, manipulate=False,
                multi=False, check_keys=False, **kwargs):
        validate_is_mapping('spec', spec)
        validate_is_mapping('document', document)

        updated_existing = False
        upserted_id = None
        num_updated = 0
        for existing_document in itertools.chain(self._iter_documents(spec), [None]):
            # we need was_insert for the setOnInsert update operation
            was_insert = False
            # the sentinel document means we should do an upsert
            if existing_document is None:
                if not upsert or num_updated:
                    continue
                _id = document.get('_id')
                to_insert = dict(spec, _id=_id) if _id else spec
                to_insert = self._expand_dots(to_insert)
                upserted_id = self._insert(self._discard_operators(to_insert))
                existing_document = self._documents[upserted_id]
                was_insert = True
            else:
                updated_existing = True
            num_updated += 1
            first = True
            subdocument = None
            for k, v in iteritems(document):
                if k in _updaters.keys():
                    updater = _updaters[k]
                    subdocument = self._update_document_fields_with_positional_awareness(
                        existing_document, v, spec, updater, subdocument)

                elif k == '$setOnInsert':
                    if not was_insert:
                        continue
                    subdocument = self._update_document_fields_with_positional_awareness(
                        existing_document, v, spec, _set_updater, subdocument)

                elif k == '$unset':
                    for field, value in iteritems(v):
                        if self._has_key(existing_document, field):
                            self._remove_key(existing_document, field)

                elif k == '$currentDate':
                    for value in itervalues(v):
                        if value == {'$type': 'timestamp'}:
                            raise NotImplementedError('timestamp is not supported so far')

                    subdocument = self._update_document_fields_with_positional_awareness(
                        existing_document, v, spec, _current_date_updater, subdocument)

                elif k == '$addToSet':
                    for field, value in iteritems(v):
                        nested_field_list = field.rsplit('.')
                        if len(nested_field_list) == 1:
                            if field not in existing_document:
                                existing_document[field] = []
                            # document should be a list append to it
                            if isinstance(value, dict):
                                if '$each' in value:
                                    # append the list to the field
                                    existing_document[field] += [
                                        obj for obj in list(value['$each'])
                                        if obj not in existing_document[field]]
                                    continue
                            if value not in existing_document[field]:
                                existing_document[field].append(value)
                            continue
                        # push to array in a nested attribute
                        else:
                            # create nested attributes if they do not exist
                            subdocument = existing_document
                            for field in nested_field_list[:-1]:
                                if field not in subdocument:
                                    subdocument[field] = {}

                                subdocument = subdocument[field]

                            # we're pushing a list
                            push_results = []
                            if nested_field_list[-1] in subdocument:
                                # if the list exists, then use that list
                                push_results = subdocument[
                                    nested_field_list[-1]]

                            if isinstance(value, dict) and '$each' in value:
                                push_results += [
                                    obj for obj in list(value['$each'])
                                    if obj not in push_results]
                            elif value not in push_results:
                                push_results.append(value)

                            subdocument[nested_field_list[-1]] = push_results
                elif k == '$pull':
                    for field, value in iteritems(v):
                        nested_field_list = field.rsplit('.')
                        # nested fields includes a positional element
                        # need to find that element
                        if '$' in nested_field_list:
                            if not subdocument:
                                subdocument = self._get_subdocument(
                                    existing_document, spec, nested_field_list)

                            # value should be a dictionary since we're pulling
                            pull_results = []
                            # and the last subdoc should be an array
                            for obj in subdocument[nested_field_list[-1]]:
                                if isinstance(obj, dict):
                                    for pull_key, pull_value in iteritems(value):
                                        if obj[pull_key] != pull_value:
                                            pull_results.append(obj)
                                    continue
                                if obj != value:
                                    pull_results.append(obj)

                            # cannot write to doc directly as it doesn't save to
                            # existing_document
                            subdocument[nested_field_list[-1]] = pull_results
                        else:
                            arr = existing_document
                            for field in nested_field_list:
                                if field not in arr:
                                    break
                                arr = arr[field]
                            if not isinstance(arr, list):
                                continue

                            if isinstance(value, dict):
                                for idx, obj in enumerate(arr):
                                    if filter_applies(value, obj):
                                        del arr[idx]
                            else:
                                for idx, obj in enumerate(arr):
                                    if value == obj:
                                        del arr[idx]
                elif k == '$pullAll':
                    for field, value in iteritems(v):
                        nested_field_list = field.rsplit('.')
                        if len(nested_field_list) == 1:
                            if field in existing_document:
                                arr = existing_document[field]
                                existing_document[field] = [
                                    obj for obj in arr if obj not in value]
                            continue
                        else:
                            subdocument = existing_document
                            for nested_field in nested_field_list[:-1]:
                                if nested_field not in subdocument:
                                    break
                                subdocument = subdocument[nested_field]

                            if nested_field_list[-1] in subdocument:
                                arr = subdocument[nested_field_list[-1]]
                                subdocument[nested_field_list[-1]] = [
                                    obj for obj in arr if obj not in value]
                elif k == '$push':
                    for field, value in iteritems(v):
                        nested_field_list = field.rsplit('.')
                        if len(nested_field_list) == 1:
                            if field not in existing_document:
                                existing_document[field] = []
                            # document should be a list
                            # append to it
                            if isinstance(value, dict):
                                if '$each' in value:
                                    # append the list to the field
                                    existing_document[field] += list(value['$each'])
                                    continue
                            existing_document[field].append(value)
                            continue
                        # nested fields includes a positional element
                        # need to find that element
                        elif '$' in nested_field_list:
                            if not subdocument:
                                subdocument = self._get_subdocument(
                                    existing_document, spec, nested_field_list)

                            # we're pushing a list
                            push_results = []
                            if nested_field_list[-1] in subdocument:
                                # if the list exists, then use that list
                                push_results = subdocument[nested_field_list[-1]]

                            if isinstance(value, dict):
                                # check to see if we have the format
                                # { '$each': [] }
                                if '$each' in value:
                                    push_results += list(value['$each'])
                                else:
                                    push_results.append(value)
                            else:
                                push_results.append(value)

                            # cannot write to doc directly as it doesn't save to
                            # existing_document
                            subdocument[nested_field_list[-1]] = push_results
                        # push to array in a nested attribute
                        else:
                            # create nested attributes if they do not exist
                            subdocument = existing_document
                            for field in nested_field_list[:-1]:
                                if field not in subdocument:
                                    subdocument[field] = {}
                                subdocument = subdocument[field]

                            # we're pushing a list
                            push_results = []
                            if nested_field_list[-1] in subdocument:
                                # if the list exists, then use that list
                                push_results = subdocument[nested_field_list[-1]]

                            if isinstance(value, dict) and '$each' in value:
                                push_results += list(value['$each'])
                            else:
                                push_results.append(value)

                            subdocument[nested_field_list[-1]] = push_results
                else:
                    if first:
                        # replace entire document
                        for key in document.keys():
                            if key.startswith('$'):
                                # can't mix modifiers with non-modifiers in
                                # update
                                raise ValueError('field names cannot start with $ [{}]'.format(k))
                        _id = spec.get('_id', existing_document.get('_id'))
                        existing_document.clear()
                        if _id:
                            existing_document['_id'] = _id
                        existing_document.update(self._internalize_dict(document))
                        if existing_document['_id'] != _id:
                            raise OperationFailure(
                                "The _id field cannot be changed from {0} to {1}"
                                .format(existing_document['_id'], _id))
                        break
                    else:
                        # can't mix modifiers with non-modifiers in update
                        raise ValueError(
                            'Invalid modifier specified: {}'.format(k))
                first = False
            if not multi:
                break

        return {
            text_type("connectionId"): self._database.client._id,
            text_type("err"): None,
            text_type("n"): num_updated,
            text_type("nModified"): num_updated if updated_existing else 0,
            text_type("ok"): 1,
            text_type("upserted"): upserted_id,
            text_type("updatedExisting"): updated_existing,
        }

    def _get_subdocument(self, existing_document, spec, nested_field_list):
        """This method retrieves the subdocument of the existing_document.nested_field_list.

        It uses the spec to filter through the items. It will continue to grab nested documents
        until it can go no further. It will then return the subdocument that was last saved.
        '$' is the positional operator, so we use the $elemMatch in the spec to find the right
        subdocument in the array.
        """
        # current document in view
        doc = existing_document
        # previous document in view
        subdocument = existing_document
        # current spec in view
        subspec = spec
        # walk down the dictionary
        for subfield in nested_field_list:
            if subfield == '$':
                # positional element should have the equivalent elemMatch in the
                # query
                subspec = subspec['$elemMatch']
                for item in doc:
                    # iterate through
                    if filter_applies(subspec, item):
                        # found the matching item save the parent
                        subdocument = doc
                        # save the item
                        doc = item
                        break
                continue

            subdocument = doc
            doc = doc[subfield]
            if subfield not in subspec:
                break
            subspec = subspec[subfield]

        return subdocument

    def _expand_dots(self, doc):
        expanded = {}
        paths = {}
        for k, v in iteritems(doc):
            key_parts = k.split('.')
            sub_doc = v
            for i in reversed(range(1, len(key_parts))):
                key = key_parts[i]
                sub_doc = {key: sub_doc}
            key = key_parts[0]
            if key in expanded:
                raise WriteError("cannot infer query fields to set, "
                                 "both paths '%s' and '%s' are matched"
                                 % (k, paths[key]))
            paths[key] = k
            expanded[key] = sub_doc
        return expanded

    def _discard_operators(self, doc):
        # TODO(this looks a little too naive...)
        return {k: v for k, v in iteritems(doc) if not k.startswith("$")}

    def find(self, filter=None, projection=None, skip=0, limit=0,
             no_cursor_timeout=False, cursor_type=None, sort=None,
             allow_partial_results=False, oplog_replay=False, modifiers=None,
             batch_size=0, manipulate=True):
        spec = filter
        if spec is None:
            spec = {}
        validate_is_mapping('filter', spec)
        return Cursor(self, functools.partial(
            self._get_dataset, spec, sort, projection, dict, skip), limit=limit)

    def _get_dataset(self, spec, sort, fields, as_class, skip):
        dataset = (self._copy_only_fields(document, fields, as_class)
                   for document in self._iter_documents(spec))
        if sort:
            for sortKey, sortDirection in reversed(sort):
                dataset = iter(sorted(
                    dataset, key=lambda x: _resolve_sort_key(sortKey, x),
                    reverse=sortDirection < 0))
        for i in xrange(skip):
            try:
                next(dataset)
            except StopIteration:
                pass

        return dataset

    def _copy_field(self, obj, container):
        if isinstance(obj, list):
            new = []
            for item in obj:
                new.append(self._copy_field(item, container))
            return new
        if isinstance(obj, dict):
            new = container()
            for key, value in obj.items():
                new[key] = self._copy_field(value, container)
            return new
        else:
            return copy.copy(obj)

    def _extract_projection_operators(self, fields):
        """Removes and returns fields with projection operators."""
        result = {}
        allowed_projection_operators = set(['$elemMatch'])
        for key, value in iteritems(fields):
            if isinstance(value, dict):
                for op in value:
                    if op not in allowed_projection_operators:
                        raise ValueError('Unsupported projection option: {}'.format(op))
                result[key] = value

        for key in result:
            del fields[key]

        return result

    def _apply_projection_operators(self, ops, doc, doc_copy):
        """Applies projection operators to copied document."""
        for field, op in iteritems(ops):
            if field not in doc_copy:
                if field in doc:
                    # field was not copied yet (since we are in include mode)
                    doc_copy[field] = doc[field]
                else:
                    # field doesn't exist in original document, no work to do
                    continue

            if '$elemMatch' in op:
                if isinstance(doc_copy[field], list):
                    # find the first item that matches
                    matched = False
                    for item in doc_copy[field]:
                        if filter_applies(op['$elemMatch'], item):
                            matched = True
                            doc_copy[field] = [item]
                            break

                    # nothing have matched
                    if not matched:
                        del doc_copy[field]

                else:
                    # remove the field since there is nothing to iterate
                    del doc_copy[field]

    def _copy_only_fields(self, doc, fields, container):
        """Copy only the specified fields."""

        if fields is None:
            return self._copy_field(doc, container)
        else:
            if not fields:
                fields = {"_id": 1}
            if not isinstance(fields, dict):
                fields = helpers._fields_list_to_dict(fields)

            # we can pass in something like {"_id":0, "field":1}, so pull the id
            # value out and hang on to it until later
            id_value = fields.pop('_id', 1)

            # filter out fields with projection operators, we will take care of them later
            projection_operators = self._extract_projection_operators(fields)

            # other than the _id field, all fields must be either includes or
            # excludes, this can evaluate to 0
            if len(set(list(fields.values()))) > 1:
                raise ValueError(
                    'You cannot currently mix including and excluding fields.')

            # if we have novalues passed in, make a doc_copy based on the
            # id_value
            if len(list(fields.values())) == 0:
                if id_value == 1:
                    doc_copy = container()
                else:
                    doc_copy = self._copy_field(doc, container)
            # if 1 was passed in as the field values, include those fields
            elif list(fields.values())[0] == 1:
                doc_copy = container()
                for key in fields:
                    key_parts = key.split('.')
                    subdocument = doc
                    subdocument_copy = doc_copy
                    full_key_path_found = True
                    for key_part in key_parts[:-1]:
                        if key_part not in subdocument:
                            full_key_path_found = False
                            break
                        subdocument = subdocument[key_part]
                        subdocument_copy = subdocument_copy.setdefault(key_part, {})
                    if not full_key_path_found or key_parts[-1] not in subdocument:
                        continue
                    subdocument_copy[key_parts[-1]] = subdocument[key_parts[-1]]
            # otherwise, exclude the fields passed in
            else:
                doc_copy = self._copy_field(doc, container)
                for key in fields:
                    key_parts = key.split('.')
                    subdocument_copy = doc_copy
                    full_key_path_found = True
                    for key_part in key_parts[:-1]:
                        if key_part not in subdocument_copy:
                            full_key_path_found = False
                            break
                        subdocument_copy = subdocument_copy[key_part]
                    if not full_key_path_found or key_parts[-1] not in subdocument_copy:
                        continue
                    del subdocument_copy[key_parts[-1]]

            # set the _id value if we requested it, otherwise remove it
            if id_value == 0:
                doc_copy.pop('_id', None)
            else:
                if '_id' in doc:
                    doc_copy['_id'] = doc['_id']

            fields['_id'] = id_value  # put _id back in fields

            # time to apply the projection operators and put back their fields
            self._apply_projection_operators(projection_operators, doc, doc_copy)
            for field, op in iteritems(projection_operators):
                fields[field] = op
            return doc_copy

    def _update_document_fields(self, doc, fields, updater):
        """Implements the $set behavior on an existing document"""
        for k, v in iteritems(fields):
            self._update_document_single_field(doc, k, v, updater)

    def _update_document_fields_positional(self, doc, fields, spec, updater,
                                           subdocument=None):
        """Implements the $set behavior on an existing document"""
        for k, v in iteritems(fields):
            if '$' in k:

                field_name_parts = k.split('.')
                if not subdocument:
                    current_doc = doc
                    subspec = spec
                    for part in field_name_parts[:-1]:
                        if part == '$':
                            subspec = subspec.get('$elemMatch', subspec)
                            for item in current_doc:
                                if filter_applies(subspec, item):
                                    current_doc = item
                                    break
                            continue

                        new_spec = {}
                        for el in subspec:
                            if el.startswith(part):
                                if len(el.split(".")) > 1:
                                    new_spec[".".join(
                                        el.split(".")[1:])] = subspec[el]
                                else:
                                    new_spec = subspec[el]
                        subspec = new_spec
                        current_doc = current_doc[part]

                    subdocument = current_doc
                    if (field_name_parts[-1] == '$' and
                            isinstance(subdocument, list)):
                        for i, doc in enumerate(subdocument):
                            if filter_applies(subspec, doc):
                                subdocument[i] = v
                                break
                        continue

                updater(subdocument, field_name_parts[-1], v)
                continue
            # otherwise, we handle it the standard way
            self._update_document_single_field(doc, k, v, updater)

        return subdocument

    def _update_document_fields_with_positional_awareness(self, existing_document, v, spec,
                                                          updater, subdocument):
        positional = any('$' in key for key in iterkeys(v))

        if positional:
            return self._update_document_fields_positional(
                existing_document, v, spec, updater, subdocument)
        self._update_document_fields(existing_document, v, updater)
        return subdocument

    def _update_document_single_field(self, doc, field_name, field_value, updater):
        field_name_parts = field_name.split(".")
        for part in field_name_parts[:-1]:
            if isinstance(doc, list):
                try:
                    if part == '$':
                        doc = doc[0]
                    else:
                        doc = doc[int(part)]
                    continue
                except ValueError:
                    pass
            elif isinstance(doc, dict):
                doc = doc.setdefault(part, {})
            else:
                return
        field_name = field_name_parts[-1]
        if isinstance(doc, list):
            try:
                doc[int(field_name)] = field_value
            except IndexError:
                pass
        else:
            updater(doc, field_name, field_value)

    def _iter_documents(self, filter=None):
        return (document for document in list(itervalues(self._documents))
                if filter_applies(filter, document))

    def find_one(self, filter=None, *args, **kwargs):
        # Allow calling find_one with a non-dict argument that gets used as
        # the id for the query.
        if filter is None:
            filter = {}
        if not isinstance(filter, collections.Mapping):
            filter = {'_id': filter}

        try:
            return next(self.find(filter, *args, **kwargs))
        except StopIteration:
            return None

    def find_one_and_delete(self, filter, projection=None, sort=None, **kwargs):
        kwargs['remove'] = True
        validate_is_mapping('filter', filter)
        return self._find_and_modify(filter, projection, sort=sort, **kwargs)

    def find_one_and_replace(self, filter, replacement,
                             projection=None, sort=None, upsert=False,
                             return_document=ReturnDocument.BEFORE, **kwargs):
        validate_is_mapping('filter', filter)
        validate_ok_for_replace(replacement)
        return self._find_and_modify(filter, projection, replacement, upsert,
                                     sort, return_document, **kwargs)

    def find_one_and_update(self, filter, update,
                            projection=None, sort=None, upsert=False,
                            return_document=ReturnDocument.BEFORE, **kwargs):
        validate_is_mapping('filter', filter)
        validate_ok_for_update(update)
        return self._find_and_modify(filter, projection, update, upsert,
                                     sort, return_document, **kwargs)

    def find_and_modify(self, query={}, update=None, upsert=False, sort=None,
                        full_response=False, manipulate=False, **kwargs):
        warnings.warn("find_and_modify is deprecated, use find_one_and_delete"
                      ", find_one_and_replace, or find_one_and_update instead",
                      DeprecationWarning, stacklevel=2)
        return self._find_and_modify(query, update=update, upsert=upsert,
                                     sort=sort, **kwargs)

    def _find_and_modify(self, query, projection=None, update=None,
                         upsert=False, sort=None,
                         return_document=ReturnDocument.BEFORE, **kwargs):
        remove = kwargs.get("remove", False)
        if kwargs.get("new", False) and remove:
            # message from mongodb
            raise OperationFailure("remove and returnNew can't co-exist")

        if not (remove or update):
            raise ValueError("Must either update or remove")

        if remove and update:
            raise ValueError("Can't do both update and remove")

        old = self.find_one(query, projection=projection, sort=sort)
        if not old and not upsert:
            return

        if old and '_id' in old:
            query = {'_id': old['_id']}

        if remove:
            self.delete_one(query)
        else:
            self._update(query, update, upsert)

        if return_document is ReturnDocument.AFTER or kwargs.get('new'):
            return self.find_one(query, projection)
        return old

    def save(self, to_save, manipulate=True, check_keys=True, **kwargs):
        warnings.warn("save is deprecated. Use insert_one or replace_one "
                      "instead", DeprecationWarning, stacklevel=2)
        validate_is_mutable_mapping("to_save", to_save)
        validate_write_concern_params(**kwargs)

        if "_id" not in to_save:
            return self.insert(to_save)
        else:
            self._update({"_id": to_save["_id"]}, to_save, True,
                         manipulate, check_keys=True, **kwargs)
            return to_save.get("_id", None)

    def delete_one(self, filter):
        validate_is_mapping('filter', filter)
        return DeleteResult(self._delete(filter), True)

    def delete_many(self, filter):
        validate_is_mapping('filter', filter)
        return DeleteResult(self._delete(filter, multi=True), True)

    def _delete(self, filter, multi=False):
        if filter is None:
            filter = {}
        if not isinstance(filter, collections.Mapping):
            filter = {'_id': filter}
        to_delete = list(self.find(filter))
        deleted_count = 0
        for doc in to_delete:
            doc_id = doc['_id']
            if isinstance(doc_id, dict):
                doc_id = helpers.hashdict(doc_id)
            del self._documents[doc_id]
            deleted_count += 1
            if not multi:
                break

        return {
            "connectionId": self._database.client._id,
            "n": deleted_count,
            "ok": 1.0,
            "err": None,
        }

    def remove(self, spec_or_id=None, multi=True, **kwargs):
        warnings.warn("remove is deprecated. Use delete_one or delete_many "
                      "instead.", DeprecationWarning, stacklevel=2)
        validate_write_concern_params(**kwargs)
        return self._delete(spec_or_id, multi=multi)

    def count(self, filter=None, **kwargs):
        if filter is None:
            return len(self._documents)
        else:
            return self.find(filter).count()

    def drop(self):
        del self._documents
        self._documents = {}

    def ensure_index(self, key_or_list, cache_for=300, **kwargs):
        self.create_index(key_or_list, cache_for, **kwargs)

    def create_index(self, key_or_list, cache_for=300, **kwargs):
        if 'unique' in kwargs and kwargs['unique']:
            self._uniques.append(helpers._index_list(key_or_list))

    def drop_index(self, index_or_name):
        pass

    def index_information(self):
        return {}

    def map_reduce(self, map_func, reduce_func, out, full_response=False,
                   query=None, limit=0):
        if execjs is None:
            raise NotImplementedError(
                "PyExecJS is required in order to run Map-Reduce. "
                "Use 'pip install pyexecjs pymongo' to support Map-Reduce mock."
            )
        if limit == 0:
            limit = None
        start_time = time.clock()
        out_collection = None
        reduced_rows = None
        full_dict = {
            'counts': {
                'input': 0,
                'reduce': 0,
                'emit': 0,
                'output': 0},
            'timeMillis': 0,
            'ok': 1.0,
            'result': None}
        map_ctx = execjs.compile("""
            function doMap(fnc, docList) {
                var mappedDict = {};
                function emit(key, val) {
                    if (key['$oid']) {
                        mapped_key = '$oid' + key['$oid'];
                    }
                    else {
                        mapped_key = key;
                    }
                    if(!mappedDict[mapped_key]) {
                        mappedDict[mapped_key] = [];
                    }
                    mappedDict[mapped_key].push(val);
                }
                mapper = eval('('+fnc+')');
                var mappedList = new Array();
                for(var i=0; i<docList.length; i++) {
                    var thisDoc = eval('('+docList[i]+')');
                    var mappedVal = (mapper).call(thisDoc);
                }
                return mappedDict;
            }
        """)
        reduce_ctx = execjs.compile("""
            function doReduce(fnc, docList) {
                var reducedList = new Array();
                reducer = eval('('+fnc+')');
                for(var key in docList) {
                    var reducedVal = {'_id': key,
                            'value': reducer(key, docList[key])};
                    reducedList.push(reducedVal);
                }
                return reducedList;
            }
        """)
        doc_list = [json.dumps(doc, default=json_util.default)
                    for doc in self.find(query)]
        mapped_rows = map_ctx.call('doMap', map_func, doc_list)
        reduced_rows = reduce_ctx.call('doReduce', reduce_func, mapped_rows)[:limit]
        for reduced_row in reduced_rows:
            if reduced_row['_id'].startswith('$oid'):
                reduced_row['_id'] = ObjectId(reduced_row['_id'][4:])
        reduced_rows = sorted(reduced_rows, key=lambda x: x['_id'])
        if full_response:
            full_dict['counts']['input'] = len(doc_list)
            for key in mapped_rows.keys():
                emit_count = len(mapped_rows[key])
                full_dict['counts']['emit'] += emit_count
                if emit_count > 1:
                    full_dict['counts']['reduce'] += 1
            full_dict['counts']['output'] = len(reduced_rows)
        if isinstance(out, (str, bytes)):
            out_collection = getattr(self._database, out)
            out_collection.drop()
            out_collection.insert(reduced_rows)
            ret_val = out_collection
            full_dict['result'] = out
        elif isinstance(out, SON) and out.get('replace') and out.get('db'):
            # Must be of the format SON([('replace','results'),('db','outdb')])
            out_db = getattr(self._database._client, out['db'])
            out_collection = getattr(out_db, out['replace'])
            out_collection.insert(reduced_rows)
            ret_val = out_collection
            full_dict['result'] = {'db': out['db'], 'collection': out['replace']}
        elif isinstance(out, dict) and out.get('inline'):
            ret_val = reduced_rows
            full_dict['result'] = reduced_rows
        else:
            raise TypeError("'out' must be an instance of string, dict or bson.SON")
        full_dict['timeMillis'] = int(round((time.clock() - start_time) * 1000))
        if full_response:
            ret_val = full_dict
        return ret_val

    def inline_map_reduce(self, map_func, reduce_func, full_response=False,
                          query=None, limit=0):
        return self.map_reduce(
            map_func, reduce_func, {'inline': 1}, full_response, query, limit)

    def distinct(self, key, filter=None):
        return self.find(filter).distinct(key)

    def group(self, key, condition, initial, reduce, finalize=None):
        if execjs is None:
            raise NotImplementedError(
                "PyExecJS is required in order to use group. "
                "Use 'pip install pyexecjs pymongo' to support group mock."
            )
        reduce_ctx = execjs.compile("""
            function doReduce(fnc, docList) {
                reducer = eval('('+fnc+')');
                for(var i=0, l=docList.length; i<l; i++) {
                    try {
                        reducedVal = reducer(docList[i-1], docList[i]);
                    }
                    catch (err) {
                        continue;
                    }
                }
            return docList[docList.length - 1];
            }
        """)

        ret_array = []
        doc_list_copy = []
        ret_array_copy = []
        reduced_val = {}
        doc_list = [doc for doc in self.find(condition)]
        for doc in doc_list:
            doc_copy = copy.deepcopy(doc)
            for k in doc:
                if isinstance(doc[k], ObjectId):
                    doc_copy[k] = str(doc[k])
                if k not in key and k not in reduce:
                    del doc_copy[k]
            for initial_key in initial:
                if initial_key in doc.keys():
                    pass
                else:
                    doc_copy[initial_key] = initial[initial_key]
            doc_list_copy.append(doc_copy)
        doc_list = doc_list_copy
        for k in key:
            doc_list = sorted(doc_list, key=lambda x: _resolve_key(k, x))
        for k in key:
            if not isinstance(k, helpers.basestring):
                raise TypeError(
                    "Keys must be a list of key names, "
                    "each an instance of %s" % helpers.basestring.__name__)
            for k2, group in itertools.groupby(doc_list, lambda item: item[k]):
                group_list = ([x for x in group])
                reduced_val = reduce_ctx.call('doReduce', reduce, group_list)
                ret_array.append(reduced_val)
        for doc in ret_array:
            doc_copy = copy.deepcopy(doc)
            for k in doc:
                if k not in key and k not in initial.keys():
                    del doc_copy[k]
            ret_array_copy.append(doc_copy)
        ret_array = ret_array_copy
        return ret_array

    def _get_group_id_fields(self, keys, parent=''):
        date_operators = [
            '$dayOfYear',
            '$dayOfMonth',
            '$dayOfWeek',
            '$year',
            '$month',
            '$week',
            '$hour',
            '$minute',
            '$second',
            '$millisecond']

        fields = []

        if isinstance(keys, dict):
            for k, v in keys.items():
                if isinstance(v, string_types):
                    if k in date_operators:
                        fields.append((parent + '__' + k + '_' + v).replace('$', ''))
                    else:
                        fields.append(v.replace('$', ''))
                elif isinstance(v, dict):
                    fields.extend(self._get_group_id_fields(v, parent + '__' + k if parent else k))
        elif isinstance(keys, str):
            fields.append(keys.replace('$', ''))

        return fields

    def _add_group_id_fields(self, out_collection, group_func_keys):
        date_operators = [
            'dayOfYear',
            'dayOfMonth',
            'dayOfWeek',
            'year',
            'month',
            'week',
            'hour',
            'minute',
            'second',
            'millisecond']

        clear_group_func_keys = []
        for key in group_func_keys:
            out_field = key.split('__')[0]

            for doc in out_collection:
                if '__' in key:
                    func_field = key.split('__')[1]
                    func, in_field = func_field.split('_')
                    out_value = doc.get(in_field)

                    if func in date_operators:
                        if func == 'dayOfYear':
                            out_value = out_value.timetuple().tm_yday
                        elif func == 'dayOfMonth':
                            out_value = out_value.day
                        elif func == 'dayOfWeek':
                            out_value = out_value.isoweekday()
                        elif func == 'year':
                            out_value = out_value.year
                        elif func == 'month':
                            out_value = out_value.month
                        elif func == 'week':
                            out_value = out_value.isocalendar()[1]
                        elif func == 'hour':
                            out_value = out_value.hour
                        elif func == 'minute':
                            out_value = out_value.minute
                        elif func == 'second':
                            out_value = out_value.second
                        elif func == 'millisecond':
                            out_value = int(out_value.microsecond / 1000)

                    doc[out_field] = out_value

            clear_group_func_keys.append(out_field)

        return out_collection, clear_group_func_keys

    def aggregate(self, pipeline, **kwargs):
        pipeline_operators = [
            '$project',
            '$match',
            '$redact',
            '$limit',
            '$skip',
            '$unwind',
            '$group',
            '$sort',
            '$geoNear',
            '$out']
        group_operators = [
            '$addToSet',
            '$first',
            '$last',
            '$max',
            '$min',
            '$avg',
            '$push',
            '$sum']
        boolean_operators = ['$and', '$or', '$not']  # noqa
        set_operators = [  # noqa
            '$setEquals',
            '$setIntersection',
            '$setDifference',
            '$setUnion',
            '$setIsSubset',
            '$anyElementTrue',
            '$allElementsTrue']
        compairison_operators = [  # noqa
            '$cmp',
            '$eq',
            '$gt',
            '$gte',
            '$lt',
            '$lte',
            '$ne']
        aritmetic_operators = [  # noqa
            '$add',
            '$divide',
            '$mod',
            '$multiply',
            '$subtract']
        string_operators = [  # noqa
            '$concat',
            '$strcasecmp',
            '$substr',
            '$toLower',
            '$toUpper']
        text_search_operators = ['$meta']  # noqa
        array_operators = ['$size']  # noqa
        projection_operators = ['$map', '$let', '$literal']  # noqa
        date_operators = [  # noqa
            '$dayOfYear',
            '$dayOfMonth',
            '$dayOfWeek',
            '$year',
            '$month',
            '$week',
            '$hour',
            '$minute',
            '$second',
            '$millisecond']
        conditional_operators = ['$cond', '$ifNull']  # noqa

        out_collection = [doc for doc in self.find()]
        grouped_collection = []
        for expression in pipeline:
            for k, v in iteritems(expression):
                if k == '$match':
                    out_collection = [doc for doc in out_collection
                                      if filter_applies(v, doc)]
                elif k == '$group':
                    _id = expression['$group']['_id']
                    group_func_keys = self._get_group_id_fields(_id)

                    out_collection, group_func_keys = self._add_group_id_fields(out_collection,
                                                                                group_func_keys)

                    if len(group_func_keys) == 0:
                        grouped_collection = []
                    else:
                        out_collection = sorted(out_collection,
                                                key=itemgetter(*map(lambda x: x.split('.')[0],
                                                                    group_func_keys)))

                    for field, value in iteritems(v):
                        if field == '_id':
                            continue
                        for func, key in iteritems(value):
                            if func in ("$sum", "$avg", "$min", "$max", "$first", "$last"):
                                if len(group_func_keys) == 0:
                                    grouped = itertools.groupby(out_collection)
                                else:
                                    grouped = itertools.groupby(out_collection,
                                                                helpers.embedded_item_getter(
                                                                    *group_func_keys))

                                for ret_value, group in grouped:
                                    group_list = ([x for x in group])
                                    if len(group_func_keys) == 0:
                                        doc_id = None
                                    else:
                                        ret_value = ret_value if isinstance(ret_value, tuple)\
                                            else [ret_value]
                                        doc_id = {k: v for (k, v) in zip(_id.keys(), ret_value)}\
                                            if isinstance(_id, dict) else ret_value[0]

                                    doc_dict = {'_id': doc_id}

                                    new_doc = True
                                    for doc in grouped_collection:
                                        if doc['_id'] == doc_id:
                                            doc_dict = doc
                                            new_doc = False
                                            break

                                    from_field = key.replace('$', '')
                                    if func == "$sum":
                                        current_val = doc_dict.get(field, 0) + \
                                            sum([doc.get(from_field, 0) for doc in group_list])
                                        doc_dict[field] = current_val
                                    elif func == "$avg":
                                        current_val = doc_dict.get(field, 0) + \
                                            sum([doc.get(from_field, 0) for doc in group_list])
                                        current_avg = current_val / max(len(group_list), 1)
                                        doc_dict[field] = current_avg
                                    elif func == "$min":
                                        current_val = doc_dict.get(field, MAXSIZE)
                                        min_doc = min([doc.get(from_field, MAXSIZE) for doc
                                                      in group_list])
                                        doc_dict[field] = min(current_val, min_doc)
                                    elif func == "$max":
                                        current_val = doc_dict.get(field, -MAXSIZE)
                                        max_doc = max([doc.get(from_field, -MAXSIZE) for doc
                                                      in group_list])
                                        doc_dict[field] = max(current_val, max_doc)
                                    elif func == "$first":
                                        current_val = doc_dict.get(field, datetime.max)
                                        min_doc = min([doc.get(from_field, datetime.max) for doc
                                                      in group_list])
                                        doc_dict[field] = min(current_val, min_doc)
                                    elif func == "$last":
                                        current_val = doc_dict.get(field, datetime.min)
                                        max_doc = max([doc.get(from_field, datetime.min) for doc
                                                      in group_list])
                                        doc_dict[field] = max(current_val, max_doc)

                                    if new_doc:
                                        grouped_collection.append(doc_dict)
                            else:
                                if func in group_operators:
                                    raise NotImplementedError(
                                        "Although %s is a valid group operator for the "
                                        "aggregation pipeline, %s is currently not implemented "
                                        "in Mongomock." % func)
                                else:
                                    raise NotImplementedError(
                                        "%s is not a valid group operator for the aggregation "
                                        "pipeline. See http://docs.mongodb.org/manual/meta/"
                                        "aggregation-quick-reference/ for a complete list of "
                                        "valid operators." % func)
                    out_collection = grouped_collection
                elif k == '$sort':
                    sort_array = []
                    for x, y in v.items():
                        sort_array.append({x: y})
                    for sort_pair in reversed(sort_array):
                        for sortKey, sortDirection in sort_pair.items():
                            out_collection = sorted(
                                out_collection,
                                key=lambda x: _resolve_sort_key(sortKey, x),
                                reverse=sortDirection < 0)
                elif k == '$skip':
                    out_collection = out_collection[v:]
                elif k == '$limit':
                    out_collection = out_collection[:v]
                elif k == '$unwind':
                    if not isinstance(v, helpers.basestring) and v[0] != '$':
                        raise ValueError(
                            "$unwind failed: exception: field path references must be prefixed "
                            "with a '$' '%s'" % v)
                    if len(v.split('.')) > 1:
                        raise NotImplementedError(
                            "Mongmock does not currently support nested field paths in the $unwind "
                            "implementation. '%s'" % v)
                    unwound_collection = []
                    for doc in out_collection:
                        array_value = doc.get(v[1:])
                        if array_value in (None, []):
                            continue
                        elif not isinstance(array_value, list):
                            raise TypeError(
                                '$unwind must specify an array field, field: '
                                '"%s", value found: %s' % (v, array_value))
                        for field_item in array_value:
                            unwound_collection.append(copy.deepcopy(doc))
                            unwound_collection[-1][v[1:]] = field_item
                    out_collection = unwound_collection
                else:
                    if k in pipeline_operators:
                        raise NotImplementedError(
                            "Although '%s' is a valid operator for the aggregation pipeline, it is "
                            "currently not implemented in Mongomock." % k)
                    else:
                        raise NotImplementedError(
                            "%s is not a valid operator for the aggregation pipeline. "
                            "See http://docs.mongodb.org/manual/meta/aggregation-quick-reference/ "
                            "for a complete list of valid operators." % k)
        return CommandCursor(out_collection)

    def with_options(
            self, codec_options=None, read_preference=None, write_concern=None, read_concern=None):
        return self


def _resolve_key(key, doc):
    return next(iter(iter_key_candidates(key, doc)), NOTHING)


def _resolve_sort_key(key, doc):
    value = _resolve_key(key, doc)
    # see http://docs.mongodb.org/manual/reference/method/cursor.sort/#ascending-descending-sort
    if value is NOTHING:
        return 0, value

    return 1, value


class Cursor(object):

    def __init__(self, collection, dataset_factory, limit=0):
        super(Cursor, self).__init__()
        self.collection = collection
        self._factory = dataset_factory
        self._dataset = self._factory()
        # pymongo limit defaults to 0, returning everything
        self._limit = limit if limit != 0 else None
        self._skip = None

    def __iter__(self):
        return self

    def clone(self):
        return Cursor(self.collection, self._factory, self._limit)

    def __next__(self):
        if self._skip:
            for i in range(self._skip):
                next(self._dataset)
            self._skip = None
        if self._limit is not None and self._limit <= 0:
            raise StopIteration()
        if self._limit is not None:
            self._limit -= 1
        return next(self._dataset)
    next = __next__

    def sort(self, key_or_list, direction=None):
        if direction is None:
            direction = 1
        if isinstance(key_or_list, (tuple, list)):
            for sortKey, sortDirection in reversed(key_or_list):
                self._dataset = iter(
                    sorted(
                        self._dataset,
                        key=lambda x: _resolve_sort_key(
                            sortKey,
                            x),
                        reverse=sortDirection < 0))
        else:
            self._dataset = iter(
                sorted(self._dataset,
                       key=lambda x: _resolve_sort_key(key_or_list, x),
                       reverse=direction < 0))
        return self

    def count(self, with_limit_and_skip=False):
        arr = [x for x in self._dataset]
        count = len(arr)
        if with_limit_and_skip:
            if self._skip:
                count -= self._skip
            if self._limit and count > self._limit:
                count = self._limit
        self._dataset = iter(arr)
        return count

    def skip(self, count):
        self._skip = count
        return self

    def limit(self, count):
        self._limit = count if count != 0 else None
        return self

    def batch_size(self, count):
        return self

    def close(self):
        pass

    def distinct(self, key):
        if not isinstance(key, helpers.basestring):
            raise TypeError('cursor.distinct key must be a string')
        unique = set()
        unique_dict_vals = []
        for x in iter(self._dataset):
            value = _resolve_key(key, x)
            if value == NOTHING:
                continue
            if isinstance(value, dict):
                if any(dict_val == value for dict_val in unique_dict_vals):
                    continue
                unique_dict_vals.append(value)
            else:
                unique.update(
                    value if isinstance(
                        value, (tuple, list)) else [value])
        return list(unique) + unique_dict_vals

    def __getitem__(self, index):
        arr = [x for x in self._dataset]
        self._dataset = iter(arr)
        return arr[index]


def _set_updater(doc, field_name, value):
    if isinstance(value, (tuple, list)):
        value = copy.deepcopy(value)
    if isinstance(doc, dict):
        doc[field_name] = value


def _inc_updater(doc, field_name, value):
    if isinstance(doc, dict):
        doc[field_name] = doc.get(field_name, 0) + value


def _max_updater(doc, field_name, value):
    if isinstance(doc, dict):
        doc[field_name] = max(doc.get(field_name, value), value)


def _min_updater(doc, field_name, value):
    if isinstance(doc, dict):
        doc[field_name] = min(doc.get(field_name, value), value)


def _sum_updater(doc, field_name, current, result):
    if isinstance(doc, dict):
        result = current + doc.get[field_name, 0]
        return result


def _current_date_updater(doc, field_name, value):
    if isinstance(doc, dict):
        doc[field_name] = datetime.utcnow()

_updaters = {
    '$set': _set_updater,
    '$inc': _inc_updater,
    '$max': _max_updater,
    '$min': _min_updater,
}
