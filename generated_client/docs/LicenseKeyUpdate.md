# LicenseKeyUpdate


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**status** | [**LicenseStatus**](LicenseStatus.md) |  | [optional] 
**expires_at** | **datetime** |  | [optional] 
**max_activations** | **int** |  | [optional] 
**features** | **object** |  | [optional] 
**notes** | **str** |  | [optional] 

## Example

```python
from openapi_client.models.license_key_update import LicenseKeyUpdate

# TODO update the JSON string below
json = "{}"
# create an instance of LicenseKeyUpdate from a JSON string
license_key_update_instance = LicenseKeyUpdate.from_json(json)
# print the JSON string representation of the object
print(LicenseKeyUpdate.to_json())

# convert the object into a dict
license_key_update_dict = license_key_update_instance.to_dict()
# create an instance of LicenseKeyUpdate from a dict
license_key_update_from_dict = LicenseKeyUpdate.from_dict(license_key_update_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


