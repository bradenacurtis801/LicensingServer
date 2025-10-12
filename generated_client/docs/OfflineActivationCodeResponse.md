# OfflineActivationCodeResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **int** |  | 
**license_key_id** | **int** |  | 
**activation_code** | **str** |  | 
**machine_id** | **str** |  | 
**is_used** | **bool** |  | 
**expires_at** | **datetime** |  | 
**created_at** | **datetime** |  | 
**used_at** | **datetime** |  | 

## Example

```python
from openapi_client.models.offline_activation_code_response import OfflineActivationCodeResponse

# TODO update the JSON string below
json = "{}"
# create an instance of OfflineActivationCodeResponse from a JSON string
offline_activation_code_response_instance = OfflineActivationCodeResponse.from_json(json)
# print the JSON string representation of the object
print(OfflineActivationCodeResponse.to_json())

# convert the object into a dict
offline_activation_code_response_dict = offline_activation_code_response_instance.to_dict()
# create an instance of OfflineActivationCodeResponse from a dict
offline_activation_code_response_from_dict = OfflineActivationCodeResponse.from_dict(offline_activation_code_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


