# ActivationFormCreate


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**license_key** | **str** |  | 
**machine_id** | **str** |  | 
**machine_name** | **str** |  | [optional] 

## Example

```python
from openapi_client.models.activation_form_create import ActivationFormCreate

# TODO update the JSON string below
json = "{}"
# create an instance of ActivationFormCreate from a JSON string
activation_form_create_instance = ActivationFormCreate.from_json(json)
# print the JSON string representation of the object
print(ActivationFormCreate.to_json())

# convert the object into a dict
activation_form_create_dict = activation_form_create_instance.to_dict()
# create an instance of ActivationFormCreate from a dict
activation_form_create_from_dict = ActivationFormCreate.from_dict(activation_form_create_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


