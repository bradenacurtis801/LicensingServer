# APITokenCreateResponse

Response when creating a new API token - includes the actual token value

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **int** |  | 
**name** | **str** |  | 
**scopes** | [**List[TokenScope]**](TokenScope.md) |  | 
**is_active** | **bool** |  | 
**expires_at** | **datetime** |  | 
**created_at** | **datetime** |  | 
**token** | **str** |  | 

## Example

```python
from openapi_client.models.api_token_create_response import APITokenCreateResponse

# TODO update the JSON string below
json = "{}"
# create an instance of APITokenCreateResponse from a JSON string
api_token_create_response_instance = APITokenCreateResponse.from_json(json)
# print the JSON string representation of the object
print(APITokenCreateResponse.to_json())

# convert the object into a dict
api_token_create_response_dict = api_token_create_response_instance.to_dict()
# create an instance of APITokenCreateResponse from a dict
api_token_create_response_from_dict = APITokenCreateResponse.from_dict(api_token_create_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


