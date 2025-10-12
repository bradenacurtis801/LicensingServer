# APITokenUpdate


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** |  | [optional] 
**scopes** | [**List[TokenScope]**](TokenScope.md) |  | [optional] 
**is_active** | **bool** |  | [optional] 
**expires_at** | **datetime** |  | [optional] 

## Example

```python
from openapi_client.models.api_token_update import APITokenUpdate

# TODO update the JSON string below
json = "{}"
# create an instance of APITokenUpdate from a JSON string
api_token_update_instance = APITokenUpdate.from_json(json)
# print the JSON string representation of the object
print(APITokenUpdate.to_json())

# convert the object into a dict
api_token_update_dict = api_token_update_instance.to_dict()
# create an instance of APITokenUpdate from a dict
api_token_update_from_dict = APITokenUpdate.from_dict(api_token_update_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


