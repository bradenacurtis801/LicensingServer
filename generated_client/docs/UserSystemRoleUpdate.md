# UserSystemRoleUpdate


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**system_role** | [**SystemRole**](SystemRole.md) |  | 

## Example

```python
from openapi_client.models.user_system_role_update import UserSystemRoleUpdate

# TODO update the JSON string below
json = "{}"
# create an instance of UserSystemRoleUpdate from a JSON string
user_system_role_update_instance = UserSystemRoleUpdate.from_json(json)
# print the JSON string representation of the object
print(UserSystemRoleUpdate.to_json())

# convert the object into a dict
user_system_role_update_dict = user_system_role_update_instance.to_dict()
# create an instance of UserSystemRoleUpdate from a dict
user_system_role_update_from_dict = UserSystemRoleUpdate.from_dict(user_system_role_update_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


