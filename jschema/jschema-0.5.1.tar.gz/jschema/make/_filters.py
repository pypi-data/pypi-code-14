from json import dumps as json_dumps

json_dumps_filter = lambda value: json_dumps(value, indent=2, separators=(",", ": "))
upper_camel_case_filter = lambda value: "".join([word.capitalize() for word in value.split("_")])
