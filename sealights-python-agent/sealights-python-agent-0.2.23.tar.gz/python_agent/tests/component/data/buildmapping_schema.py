schema = {
    "type": "object",
    "properties": {
        "files": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "hash": {
                        "type": "string"
                    },
                    "methods": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "isAnonymous": {
                                    "type": "boolean"
                                },
                                "hash": {
                                    "type": "string"
                                },
                                "name": {
                                    "type": "string"
                                },
                                "uniqueName": {
                                    "type": "string"
                                },
                                "constructor": {
                                    "type": "boolean"
                                },
                                "position": {
                                    "type": "array",
                                    "items": {
                                        "type": "integer"
                                    }
                                },
                                "sigHash": {
                                    "type": "string"
                                },
                                "id": {
                                    "type": "string"
                                },
                                "endPosition": {
                                    "type": "array",
                                    "items": {
                                        "type": "integer"
                                    }
                                },
                                "status": {
                                    "type": "string"
                                },
                                "branches": {
                                    "type": "array",
                                    "items": {}
                                }
                            },
                            "required": [
                                "isAnonymous",
                                "hash",
                                "name",
                                "uniqueName",
                                "constructor",
                                "position",
                                "sigHash",
                                "id",
                                "endPosition",
                            ]
                        }
                    },
                    "filename": {
                        "type": "string"
                    },
                    "status": {
                        "type": "string"
                    }
                },
                "required": [
                    "hash",
                    "methods",
                    "filename"
                ]
            }
        },
        "meta": {
            "type": "object",
            "properties": {
                "appName": {
                    "type": "string"
                },
                "generated": {
                    "type": "integer"
                },
                "build": {
                    "type": "string"
                },
                "branch": {
                    "type": "string"
                },
                "technology": {
                    "type": "string"
                },
                "customerId": {
                    "type": "string"
                }
            },
            "required": [
                "appName",
                "generated",
                "build",
                "branch",
                "technology",
                "customerId"
            ]
        },
        "dependencies": {
            "type": "array",
            "items": {}
        }
    },
    "required": [
        "files",
        "meta",
        "dependencies"
    ]
}