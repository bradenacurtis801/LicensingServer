# UserBusinessRoleUpdate


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**business_role** | [**UserRole**](UserRole.md) |  | 

## Example

```python
from openapi_client.models.user_business_role_update import UserBusinessRoleUpdate

# TODO update the JSON string below
json = "{}"
# create an instance of UserBusinessRoleUpdate from a JSON string
user_business_role_update_instance = UserBusinessRoleUpdate.from_json(json)
# print the JSON string representation of the object
print(UserBusinessRoleUpdate.to_json())

# convert the object into a dict
user_business_role_update_dict = user_business_role_update_instance.to_dict()
# create an instance of UserBusinessRoleUpdate from a dict
user_business_role_update_from_dict = UserBusinessRoleUpdate.from_dict(user_business_role_update_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


