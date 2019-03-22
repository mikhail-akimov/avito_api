from jsonschema import validate, exceptions

get_all_companies_output = {
    "type": "array",
    "items": {
        "type": "object",
        "properties": {
            "id": {
                "type": "number"
            },
            "name": {
                "type": "string"
            }
        },
        "required": ["id", "name"]
    }
}

get_one_company_output = {
    "type": "object",
    "properties": {
        "id": {
            "type": "number"
        },
        "name": {
            "type": "string"
        }
    },
    "required": ["id", "name"]
}

add_company_input = {
    "type": "object",
    "properties": {
        "company_name": {
            "type": "string"
        }
    },
    "required": ["company_name"]
}

add_company_output = {
    "type": "object",
    "properties": {
        "id": {
            "type": "number"
        },
        "name": {
            "type": "string"
        }
    },
    "required": ["id", "name"]
}

get_all_employees_output = {
    "type": "array",
    "items": {
        "type": "object",
        "properties": {
            "id": {
                "type": "number"
            },
            "name": {
                "type": "string"
            },
            "company": {
                "type": ["null", "integer"]
            }
        },
        "required": ["id", "name", "company"]
    }
}

add_employee_input = {
    "type": "object",
    "properties": {
        "employee_name": {
            "type": "string"
        }
    },
    "required": ["employee_name"]
}

add_employee_output = {
    "type": "object",
    "properties": {
        "id": {
            "type": "number"
        },
        "name": {
            "type": "string"
        }
    },
    "required": ["id", "name"]
}

assign_employee_input = {
    "type": "object",
    "properties": {
        "employee_id": {
            "type": "integer"
        },
        "company_id": {
            "type": "integer"
        }
    },
    "required": ["employee_id", "company_id"]
}

assign_employee_output = {
    "type": "object",
    "properties": {
        "id": {
            "type": "integer"
        },
        "name": {
            "type": "string"
        },
        "company": {
            "type": "integer"
        },
        "phone": {
            "type": ["string", "null"]
        }
    },
    "required": ["id", "name", "company", "phone"]
}
add_item_input = {
    "type": "object",
    "properties": {
        "item_name": {
            "type": "string"
        },
        "company_id": {
            "type": "integer"
        }
    },
    "required": ["item_name", "company_id"]
}

add_item_output = {
    "type": "object",
    "properties": {
        "id": {
            "type": "integer"
        },
        "name": {
            "type": "string"
        },
        "company": {
            "type": "integer"
        }
    },
    "required": ["id", "name", "company"]
}
assign_item_input = {
    "type": "object",
    "properties": {
        "item_id": {
            "type": "integer"
        },
        "employee_id": {
            "type": "integer"
        }
    },
    "required": ["item_id", "employee_id"]
}

assign_item_output = {
    "type": "object",
    "properties": {
        "id": {
            "type": "integer"
        },
        "name": {
            "type": "string"
        },
        "company": {
            "type": "integer"
        },
        "employee": {
            "type": "integer"
        }
    },
    "required": ["id", "name", "company", "employee"]
}
