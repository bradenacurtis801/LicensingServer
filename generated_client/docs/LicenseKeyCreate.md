# LicenseKeyCreate


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**customer_id** | **int** |  | 
**application_id** | **int** |  | 
**expires_at** | **datetime** |  | [optional] 
**max_activations** | **int** |  | [optional] [default to 1]
**features** | **object** |  | [optional] 
**notes** | **str** |  | [optional] 

## Example

```python
from openapi_client.models.license_key_create import LicenseKeyCreate

# TODO update the JSON string below
json = "{}"
# create an instance of LicenseKeyCreate from a JSON string
license_key_create_instance = LicenseKeyCreate.from_json(json)
# print the JSON string representation of the object
print(LicenseKeyCreate.to_json())

# convert the object into a dict
license_key_create_dict = license_key_create_instance.to_dict()
# create an instance of LicenseKeyCreate from a dict
license_key_create_from_dict = LicenseKeyCreate.from_dict(license_key_create_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


