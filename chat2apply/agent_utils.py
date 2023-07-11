def safe_parse_arguments(args_str):
    try:
        return json.loads(args_str)
    except Exception as e:
        raise ValueError(f"invalid function_call arguments: {args_str}") from e

def parse_function_call(params):
    name = params.get('name') or ''
    _args = params.get('arguments') or '{}'
    args = safe_parse_arguments(_args)
    if is_function_valid(name):
        return name, args
    raise ValueError(f"invalid function: name={name} params={params}")

def get_func_spec(name):
    for spec in specs:
        if spec['name'] == name:
            return spec
    return {}

def is_function_valid(name):
    spec = get_func_spec(name)
    return bool(spec)


def find_invalid_argument(name, arguments):
    spec = get_func_spec(name)
    func_properties = spec['parameters']['properties']
    for key in arguments:
        value = arguments[key]
        if is_argument_valid(value, func_properties[key]['type']):
            continue
        return {
            'name': key,
            'properties': func_properties[key]
        }
    return {}
