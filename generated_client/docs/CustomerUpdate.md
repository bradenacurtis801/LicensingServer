# CustomerUpdate


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** |  | [optional] 
**email** | **str** |  | [optional] 
**company** | **str** |  | [optional] 

## Example

```python
from openapi_client.models.customer_update import CustomerUpdate

# TODO update the JSON string below
json = "{}"
# create an instance of CustomerUpdate from a JSON string
customer_update_instance = CustomerUpdate.from_json(json)
# print the JSON string representation of the object
print(CustomerUpdate.to_json())

# convert the object into a dict
customer_update_dict = customer_update_instance.to_dict()
# create an instance of CustomerUpdate from a dict
customer_update_from_dict = CustomerUpdate.from_dict(customer_update_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


