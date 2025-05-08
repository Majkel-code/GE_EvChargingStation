
import json
import jsonschema


def validate_json_schema(input_json, reference_schema_path):
    try:
        reference_schema = __get_reference_json(reference_schema_path)
        jsonschema.validate(instance=input_json,schema=reference_schema)
    except jsonschema.SchemaError as schema_err:
        raise jsonschema.SchemaError(f"Your schema on path {reference_schema_path} is not really JSON schema!")
    except jsonschema.ValidationError as val_err:
        raise jsonschema.ValidationError(f"The validation went wrong! Error: {val_err}")
    except Exception as ex:
        raise Exception(f"Something went terribly wrong! Error: {ex}")


def __get_reference_json(reference_schema_path):
    try:
        with open(reference_schema_path) as json_file:
            data = json.load(json_file)
        return data
    except json.decoder.JSONDecodeError as json_err:
        raise json.decoder.JSONDecodeError(f"I could not make json out of file {reference_schema_path}! Error: {json_err}")
    except FileNotFoundError as file_err:
        raise FileNotFoundError(f"I was not able to open file in path {reference_schema_path}! Error: {file_err}")
    except Exception as ex:
        raise Exception(f"Something went terribly wrong! Error: {ex}")
    
