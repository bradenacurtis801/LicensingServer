# CustomerCreate


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** |  | 
**email** | **str** |  | 
**company** | **str** |  | [optional] 

## Example

```python
from openapi_client.models.customer_create import CustomerCreate

# TODO update the JSON string below
json = "{}"
# create an instance of CustomerCreate from a JSON string
customer_create_instance = CustomerCreate.from_json(json)
# print the JSON string representation of the object
print(CustomerCreate.to_json())

# convert the object into a dict
customer_create_dict = customer_create_instance.to_dict()
# create an instance of CustomerCreate from a dict
customer_create_from_dict = CustomerCreate.from_dict(customer_create_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


