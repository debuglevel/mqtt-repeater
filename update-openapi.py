from app.rest.main import fastapi

openapi = fastapi.openapi()

# openapi_json_filename = "openapi.json"
# print(f"Generating {openapi_json_filename} ...")
# with open(openapi_json_filename, "w") as openapi_json_file:
#     import json
#
#     json.dump(openapi, openapi_json_file, indent=4)

openapi_yaml_filename = "openapi.yaml"
print(f"Generating {openapi_yaml_filename} ...")
with open(openapi_yaml_filename, "w") as openapi_yaml_file:
    import yaml

    yaml.dump(openapi, openapi_yaml_file)
