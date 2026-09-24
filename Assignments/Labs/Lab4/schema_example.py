import jsonschema

ORDER_SCHEMA = {
    "type": "object",
    "properties": {
        "sizes": {"type": "array", "items": {"type": "string", "enum": ["S", "M", "L"]}},
    },
    "required": ["sizes"],
}

for order in [{"sizes": ["S", "L"]}, {"sizes": ["XL"]}, {"sizes": "M"}, {}]:
    try:
        jsonschema.validate(instance=order, schema=ORDER_SCHEMA)
        print(order, "valid")
    except jsonschema.ValidationError as err:
        print(order, "invalid:", err.message)