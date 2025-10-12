# LicenseKeyResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **int** |  | 
**license_key** | **str** |  | 
**customer_id** | **int** |  | 
**application_id** | **int** |  | 
**status** | [**LicenseStatus**](LicenseStatus.md) |  | 
**expires_at** | **datetime** |  | 
**max_activations** | **int** |  | 
**current_activations** | **int** |  | 
**features** | **object** |  | 
**notes** | **str** |  | 
**created_at** | **datetime** |  | 
**updated_at** | **datetime** |  | 

## Example

```python
from openapi_client.models.license_key_response import LicenseKeyResponse

# TODO update the JSON string below
json = "{}"
# create an instance of LicenseKeyResponse from a JSON string
license_key_response_instance = LicenseKeyResponse.from_json(json)
# print the JSON string representation of the object
print(LicenseKeyResponse.to_json())

# convert the object into a dict
license_key_response_dict = license_key_response_instance.to_dict()
# create an instance of LicenseKeyResponse from a dict
license_key_response_from_dict = LicenseKeyResponse.from_dict(license_key_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


