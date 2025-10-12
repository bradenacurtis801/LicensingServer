# LicenseValidationRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**license_key** | **str** |  | 
**machine_id** | **str** |  | 

## Example

```python
from openapi_client.models.license_validation_request import LicenseValidationRequest

# TODO update the JSON string below
json = "{}"
# create an instance of LicenseValidationRequest from a JSON string
license_validation_request_instance = LicenseValidationRequest.from_json(json)
# print the JSON string representation of the object
print(LicenseValidationRequest.to_json())

# convert the object into a dict
license_validation_request_dict = license_validation_request_instance.to_dict()
# create an instance of LicenseValidationRequest from a dict
license_validation_request_from_dict = LicenseValidationRequest.from_dict(license_validation_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


