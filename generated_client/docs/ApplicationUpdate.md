# ApplicationUpdate


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** |  | [optional] 
**version** | **str** |  | [optional] 
**description** | **str** |  | [optional] 
**features** | **object** |  | [optional] 

## Example

```python
from openapi_client.models.application_update import ApplicationUpdate

# TODO update the JSON string below
json = "{}"
# create an instance of ApplicationUpdate from a JSON string
application_update_instance = ApplicationUpdate.from_json(json)
# print the JSON string representation of the object
print(ApplicationUpdate.to_json())

# convert the object into a dict
application_update_dict = application_update_instance.to_dict()
# create an instance of ApplicationUpdate from a dict
application_update_from_dict = ApplicationUpdate.from_dict(application_update_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


