
DRAFT = "http://json-schema.org/draft-04/schema#"

def Typeof(obj):
    """sort of mapping JSON/python"""

    if obj.__class__.__name__ == 'dict':
        return 'object'

    elif obj.__class__.__name__ == 'str':
        return 'string'

    elif obj.__class__.__name__ == 'function':
        return 'function'

    elif obj.__class__.__name__ == 'list':
        return 'array'

    elif obj.__class__.__name__ == 'bool':
        return 'boolean'

    elif obj.__class__.__name__ == 'int' or obj.__class__.__name__ == 'float' or obj.__class__.__name__ == 'long':
        return 'number'

    return 'null'


def getUniqueKeys(a, b, c):
    """compare a to b
     find the unique key between them
     and return it"""

    a = a.keys()

    if c == None:
        c = []

    value = []
    cIndex = 0
    aIndex = 0
    keyLength = len(b)
    keyIndex = 0

    for keys in a:
        for k in b:
            if k == keys:

                c.append(k)
                return c


def processArray(array, output, nested):
    """process to type array treatment"""

    oneof = []
    type_ = ''
    index = 0
    ind = 0
    length = len(array)
    leng = len(array)
    elementType = ''
    items = {}

    value = array[index]
    itemType = Typeof(value)
    required = []
    processOutput = {}
    properties = {}


    if nested  and output:
        items = output
        output = {}
        output['items'] = items

    else:
        if output is None:
            output = {}

        output["type"] = Typeof(array)

        if output.has_key("items") == False:

            output["items"] = {}

    while leng > index:

        elementType = Typeof(array[index])

        if type_ and elementType != type_:

            output['items'] = oneof
            oneof = True

        else :
            type_ = elementType

        index = index + 1

    if not oneof:
        items["type"] = type_
        output["items"] = items

    if type_ == 'object':

        while ind < length:

            if itemType == 'object':
                items = output["items"]
                items["properties"] = properties

                if properties:
                    items["required"] = getUniqueKeys(properties, value, required)
                    output["items"] = items

                if oneof:
                    processOutput = processObject(value, {}, True)
                else:
                    processOutput = processObject(value, items["properties"], True)

            elif itemType == 'array':
                if oneof:
                    processOutput = processArray(value, {}, True)
                else:
                    processOutput = processArray(value, items["properties"], True)

            else:
                processOutput["type"] = itemType

            ind = ind + 1

        if oneof:
            oneof.append(processOutput)
            items["oneof"] = oneof
            output["items"] = items

        else:
            items["properties"] = processOutput
            output["items"] = items

    if nested:
        return output["items"]

    else:
        return output


def processObject(obj, output, nested):
    """process to type object treatment"""

    properties = {}
    value = {}
    type_ = ''

    if nested and output:
        properties = output
        output = {}
        output["properties"] = properties

    else:
        if output is None:
            output = {}

        output["type"] = Typeof(obj)

        if output.has_key("properties") == False:

            output["properties"] = {}

    key = obj.keys()
    value = obj.values()
    index = 0
    length = len(obj)

    while index < length:
        k = key[index]
        v = value[index]

        type_ = Typeof(v)

        if type_ == 'object':
            properties[k] = processObject(v, output["properties"], nested)
            output["properties"] = properties

        elif type_ == 'array':
            properties[k] = processArray(v, output["properties"], nested)
            output["properties"] = properties

        else:
            typ = {}
            typ["type"] = type_
            properties[k] = typ
            output["properties"] = properties

        index = index + 1


    if nested == True:
        return output["properties"]

    else:
        return output


def generateSchemaJson(title, obj):
    """this function call the different process
    to teat the differentfield of the data in parameter"""

    output = {'$schema':DRAFT}
    processOutput = {}
    items = {}

    if isinstance(title, str):
        output["title"] = title

    else:
        obj = title
        title = ''

    output["type"] = Typeof(obj)

    if output["type"] == "object":
        processOutput = processObject(obj, output, False)
        output["type"] = processOutput["type"]
        output["properties"] = processOutput["properties"]

    elif output["type"] == "array":
        processOutput = processArray(obj, output, False)
        output["type"] = processOutput["type"]
        output["items"] = processOutput["items"]
        items = processOutput["items"]

        if output.has_key("title") == True:
            items["title"] = output["title"]
            output["items"] = items
            output["title"] = title + ' Set'

    return output
