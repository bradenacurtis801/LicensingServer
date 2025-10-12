# OfflineActivationCodeCreate


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**license_key_id** | **int** |  | 
**machine_id** | **str** |  | [optional] 
**quantity** | **int** |  | [optional] [default to 1]

## Example

```python
from openapi_client.models.offline_activation_code_create import OfflineActivationCodeCreate

# TODO update the JSON string below
json = "{}"
# create an instance of OfflineActivationCodeCreate from a JSON string
offline_activation_code_create_instance = OfflineActivationCodeCreate.from_json(json)
# print the JSON string representation of the object
print(OfflineActivationCodeCreate.to_json())

# convert the object into a dict
offline_activation_code_create_dict = offline_activation_code_create_instance.to_dict()
# create an instance of OfflineActivationCodeCreate from a dict
offline_activation_code_create_from_dict = OfflineActivationCodeCreate.from_dict(offline_activation_code_create_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


