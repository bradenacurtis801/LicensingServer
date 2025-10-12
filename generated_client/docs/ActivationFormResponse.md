# ActivationFormResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **int** |  | 
**license_key_id** | **int** |  | 
**machine_id** | **str** |  | 
**machine_name** | **str** |  | 
**request_code** | **str** |  | 
**activation_code** | **str** |  | 
**status** | **str** |  | 
**expires_at** | **datetime** |  | 
**created_at** | **datetime** |  | 
**completed_at** | **datetime** |  | 

## Example

```python
from openapi_client.models.activation_form_response import ActivationFormResponse

# TODO update the JSON string below
json = "{}"
# create an instance of ActivationFormResponse from a JSON string
activation_form_response_instance = ActivationFormResponse.from_json(json)
# print the JSON string representation of the object
print(ActivationFormResponse.to_json())

# convert the object into a dict
activation_form_response_dict = activation_form_response_instance.to_dict()
# create an instance of ActivationFormResponse from a dict
activation_form_response_from_dict = ActivationFormResponse.from_dict(activation_form_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


