# APITokenCreate


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** |  | 
**scopes** | [**List[TokenScope]**](TokenScope.md) |  | 
**expires_at** | **datetime** |  | [optional] 

## Example

```python
from openapi_client.models.api_token_create import APITokenCreate

# TODO update the JSON string below
json = "{}"
# create an instance of APITokenCreate from a JSON string
api_token_create_instance = APITokenCreate.from_json(json)
# print the JSON string representation of the object
print(APITokenCreate.to_json())

# convert the object into a dict
api_token_create_dict = api_token_create_instance.to_dict()
# create an instance of APITokenCreate from a dict
api_token_create_from_dict = APITokenCreate.from_dict(api_token_create_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


