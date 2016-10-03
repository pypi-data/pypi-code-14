__author__ = 'marcoantonioalberoalbero'


class TasksSchema:

    schema = {
        "$schema": "http://json-schema.org/draft-04/schema#",
        "definitions": {
            "identifier": {
                "type": "string",
                "pattern": "^[A-Za-z0-9\\.-_]+$"
            },
            "task": {
                "type": "object",
                "properties": {
                    "id": {"$ref": "#/definitions/identifier"},
                    "env": {
                        "type": "array",
                        "items": {
                            "property": {
                                "type": "string"
                            },
                            "value": {
                                "type": "string"
                            }
                        }
                    },
                    "parallel_tasks": {
                        "type": "array",
                        "items": {
                            "anyOf": [
                                {
                                    "$ref": "#/definitions/task"
                                },
                                {
                                    "$ref": "#/definitions/command"
                                }
                            ]
                        }
                    },
                    "sequential_tasks": {
                        "type": "array",
                        "items": {
                            "anyOf": [
                                {
                                    "$ref": "#/definitions/task"
                                },
                                {
                                    "$ref": "#/definitions/command"
                                }
                            ]
                        }
                    }
                },
                "required": [
                    "id"
                ],
                "anyOf": [
                    {
                        "required": ["parallel_tasks"]
                    },
                    {
                        "required": ["sequential_tasks"]
                    }
                ],
                "additionalProperties": False
            },
            "command": {
                "type": "object",
                "properties": {
                    "id": {"$ref": "#/definitions/identifier"},
                    "env": {
                        "type": "array",
                        "items": {
                            "property": {
                                "type": "string"
                            },
                            "value": {
                                "type": "string"
                            }
                        }
                    },
                    "cmd": {
                        "type": "string"
                    }
                },
                "required": [
                    "id", "cmd"
                ],
                "additionalProperties": False
            }
        },

        "type": "object",
        "properties": {
            "build": {
                "type": "string"
            },
            "starter": {
                "anyOf": [
                    {
                        "$ref": "#/definitions/task"
                    },
                    {
                        "$ref": "#/definitions/command"
                    }
                ]
            }
        },
        "required": ["build", "starter"],
        "additionalProperties": False
    }