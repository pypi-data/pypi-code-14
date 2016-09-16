# -*- coding: utf-8 -*-

from six import string_types, integer_types


class SchemaGenerator(object):
    """
    Class used to generate JSON schema from data.
    """

    DRAFT = 'http://json-schema.org/draft-04/schema#'

    class Error(Exception):
        """
        Error raised when an error occured during schema generation.
        """

    def __call__(self, obj, title=None):
        """
        Create a schema validating data.

        :param obj: input data to generate a schema from
        :type obj: any JSON serializable basic type

        :param title: Schema's title (optional)
        :type title: str

        :return: Schema validating data
        :rtype: dict

        :raises SchemaGenerator.Error: when obj contains a not valid type
        """

        output = {
            '$schema': SchemaGenerator.DRAFT
        }

        if title is not None:
            output['title'] = title

        _type = self.get_type(obj)
        output['type'] = _type

        if _type == 'array':
            result = self.process_array(obj, nested=True)
            output['items'] = result

            if title is not None:
                output['items']['title'] = title
                output['title'] = '{0} Set'.format(title)

        elif _type == 'object':
            output['properties'] = self.process_object(obj, nested=True)

        return output

    def get_type(self, obj):
        """
        Get JSON type from object.

        :param obj: Object to guess type name from.
        :type obj: any JSON serializable basic type

        :return: JSON type name
        :rtype: str

        :raises: SchemaGenerator.Error: when obj is not a valid type
        """

        if obj is None:
            return 'null'

        elif isinstance(obj, bool):
            return 'boolean'

        elif isinstance(obj, integer_types):
            return 'integer'

        elif isinstance(obj, float):
            return 'number'

        elif isinstance(obj, string_types):
            return 'string'

        elif isinstance(obj, (list, tuple)):
            return 'array'

        elif isinstance(obj, dict):
            return 'object'

        else:
            raise SchemaGenerator.Error('Unsupported data type: {0}'.format(
                obj.__class__.__name__
            ))

    def process_array(self, obj, output=None, nested=False):
        """
        Guess schema of array's items.
        """

        oneOf = False
        _type = None

        if nested and output is not None:
            output = {
                'items': output
            }

        else:
            output = output if output is not None else {}
            output['type'] = 'array'
            output['items'] = output.get('items', {})

        for item in obj:
            itemtype = self.get_type(item)

            if _type is not None and itemtype != _type:
                output['items']['oneOf'] = []
                oneOf = True
                break

            else:
                _type = itemtype

        if not oneOf:
            output['items']['type'] = _type

        if 'oneOf' in output['items'] or _type == 'object':
            for item in obj:
                itemtype = self.get_type(item)

                result = None

                if itemtype == 'object':
                    if 'properties' in output['items']:
                        output['items']['required'] = self.get_unique_keys(
                            output['items']['properties'],
                            item,
                            output['items'].get('required', [])
                        )

                    result = self.process_object(
                        item,
                        {} if oneOf else output['items'].get('properties'),
                        True
                    )

                elif itemtype == 'array':
                    result = self.process_array(
                        item,
                        {} if oneOf else output['items'].get('properties'),
                        True
                    )

                else:
                    result = {
                        'type': itemtype
                    }

                if oneOf:
                    output['items']['oneOf'].append(result)

                else:
                    output['items']['properties'] = result

        return output['items'] if nested else output

    def process_object(self, obj, output=None, nested=False):
        """
        Guess schema of object's properties.
        """

        if nested and output is not None:
            output = {
                'properties': output
            }

        else:
            output = output if output is not None else {}
            output['type'] = 'object'
            output['properties'] = output.get('properties', {})

        for key in obj:
            value = obj[key]
            valtype = self.get_type(value)

            if valtype == 'object':
                output['properties'][key] = self.process_object(value)

            elif valtype == 'array':
                output['properties'][key] = self.process_array(value)

            else:
                output['properties'][key] = {
                    'type': valtype
                }

        return output['properties'] if nested else output

    def get_unique_keys(self, properties, obj, required):
        """
        Get required keys from object.
        """

        for key in obj:
            if key not in properties:
                if key in required:
                    required.remove(key)

            elif key not in required:
                required.append(key)

        return required
