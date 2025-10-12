# LicenseValidationResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**valid** | **bool** |  | 
**license_id** | **int** |  | [optional] 
**customer_id** | **int** |  | [optional] 
**application_id** | **int** |  | [optional] 
**status** | [**LicenseStatus**](LicenseStatus.md) |  | [optional] 
**expires_at** | **datetime** |  | [optional] 
**features** | **object** |  | [optional] 
**remaining_activations** | **int** |  | [optional] 
**message** | **str** |  | [optional] 

## Example

```python
from openapi_client.models.license_validation_response import LicenseValidationResponse

# TODO update the JSON string below
json = "{}"
# create an instance of LicenseValidationResponse from a JSON string
license_validation_response_instance = LicenseValidationResponse.from_json(json)
# print the JSON string representation of the object
print(LicenseValidationResponse.to_json())

# convert the object into a dict
license_validation_response_dict = license_validation_response_instance.to_dict()
# create an instance of LicenseValidationResponse from a dict
license_validation_response_from_dict = LicenseValidationResponse.from_dict(license_validation_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


