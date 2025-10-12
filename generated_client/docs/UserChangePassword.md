# UserChangePassword


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**current_password** | **str** |  | 
**new_password** | **str** |  | 

## Example

```python
from openapi_client.models.user_change_password import UserChangePassword

# TODO update the JSON string below
json = "{}"
# create an instance of UserChangePassword from a JSON string
user_change_password_instance = UserChangePassword.from_json(json)
# print the JSON string representation of the object
print(UserChangePassword.to_json())

# convert the object into a dict
user_change_password_dict = user_change_password_instance.to_dict()
# create an instance of UserChangePassword from a dict
user_change_password_from_dict = UserChangePassword.from_dict(user_change_password_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


