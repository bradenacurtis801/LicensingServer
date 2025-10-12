# openapi_client.CustomersApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_customer_api_v1_customers_post**](CustomersApi.md#create_customer_api_v1_customers_post) | **POST** /api/v1/customers/ | Create Customer
[**delete_customer_api_v1_customers_customer_id_delete**](CustomersApi.md#delete_customer_api_v1_customers_customer_id_delete) | **DELETE** /api/v1/customers/{customer_id} | Delete Customer
[**get_customer_api_v1_customers_customer_id_get**](CustomersApi.md#get_customer_api_v1_customers_customer_id_get) | **GET** /api/v1/customers/{customer_id} | Get Customer
[**list_customers_api_v1_customers_get**](CustomersApi.md#list_customers_api_v1_customers_get) | **GET** /api/v1/customers/ | List Customers
[**update_customer_api_v1_customers_customer_id_put**](CustomersApi.md#update_customer_api_v1_customers_customer_id_put) | **PUT** /api/v1/customers/{customer_id} | Update Customer


# **create_customer_api_v1_customers_post**
> CustomerResponse create_customer_api_v1_customers_post(customer_create)

Create Customer

Create a new customer

### Example

* Bearer Authentication (HTTPBearer):

```python
import openapi_client
from openapi_client.models.customer_create import CustomerCreate
from openapi_client.models.customer_response import CustomerResponse
from openapi_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "http://localhost"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure Bearer authorization: HTTPBearer
configuration = openapi_client.Configuration(
    access_token = os.environ["BEARER_TOKEN"]
)

# Enter a context with an instance of the API client
with openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.CustomersApi(api_client)
    customer_create = openapi_client.CustomerCreate() # CustomerCreate | 

    try:
        # Create Customer
        api_response = api_instance.create_customer_api_v1_customers_post(customer_create)
        print("The response of CustomersApi->create_customer_api_v1_customers_post:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling CustomersApi->create_customer_api_v1_customers_post: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **customer_create** | [**CustomerCreate**](CustomerCreate.md)|  | 

### Return type

[**CustomerResponse**](CustomerResponse.md)

### Authorization

[HTTPBearer](../README.md#HTTPBearer)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_customer_api_v1_customers_customer_id_delete**
> delete_customer_api_v1_customers_customer_id_delete(customer_id)

Delete Customer

Delete a customer

### Example

* Bearer Authentication (HTTPBearer):

```python
import openapi_client
from openapi_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "http://localhost"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure Bearer authorization: HTTPBearer
configuration = openapi_client.Configuration(
    access_token = os.environ["BEARER_TOKEN"]
)

# Enter a context with an instance of the API client
with openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.CustomersApi(api_client)
    customer_id = 56 # int | 

    try:
        # Delete Customer
        api_instance.delete_customer_api_v1_customers_customer_id_delete(customer_id)
    except Exception as e:
        print("Exception when calling CustomersApi->delete_customer_api_v1_customers_customer_id_delete: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **customer_id** | **int**|  | 

### Return type

void (empty response body)

### Authorization

[HTTPBearer](../README.md#HTTPBearer)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**204** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_customer_api_v1_customers_customer_id_get**
> CustomerResponse get_customer_api_v1_customers_customer_id_get(customer_id)

Get Customer

Get a specific customer

### Example

* Bearer Authentication (HTTPBearer):

```python
import openapi_client
from openapi_client.models.customer_response import CustomerResponse
from openapi_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "http://localhost"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure Bearer authorization: HTTPBearer
configuration = openapi_client.Configuration(
    access_token = os.environ["BEARER_TOKEN"]
)

# Enter a context with an instance of the API client
with openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.CustomersApi(api_client)
    customer_id = 56 # int | 

    try:
        # Get Customer
        api_response = api_instance.get_customer_api_v1_customers_customer_id_get(customer_id)
        print("The response of CustomersApi->get_customer_api_v1_customers_customer_id_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling CustomersApi->get_customer_api_v1_customers_customer_id_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **customer_id** | **int**|  | 

### Return type

[**CustomerResponse**](CustomerResponse.md)

### Authorization

[HTTPBearer](../README.md#HTTPBearer)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_customers_api_v1_customers_get**
> List[CustomerResponse] list_customers_api_v1_customers_get(skip=skip, limit=limit)

List Customers

List all customers for the authenticated user

### Example

* Bearer Authentication (HTTPBearer):

```python
import openapi_client
from openapi_client.models.customer_response import CustomerResponse
from openapi_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "http://localhost"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure Bearer authorization: HTTPBearer
configuration = openapi_client.Configuration(
    access_token = os.environ["BEARER_TOKEN"]
)

# Enter a context with an instance of the API client
with openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.CustomersApi(api_client)
    skip = 0 # int |  (optional) (default to 0)
    limit = 100 # int |  (optional) (default to 100)

    try:
        # List Customers
        api_response = api_instance.list_customers_api_v1_customers_get(skip=skip, limit=limit)
        print("The response of CustomersApi->list_customers_api_v1_customers_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling CustomersApi->list_customers_api_v1_customers_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **skip** | **int**|  | [optional] [default to 0]
 **limit** | **int**|  | [optional] [default to 100]

### Return type

[**List[CustomerResponse]**](CustomerResponse.md)

### Authorization

[HTTPBearer](../README.md#HTTPBearer)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_customer_api_v1_customers_customer_id_put**
> CustomerResponse update_customer_api_v1_customers_customer_id_put(customer_id, customer_update)

Update Customer

Update a customer

### Example

* Bearer Authentication (HTTPBearer):

```python
import openapi_client
from openapi_client.models.customer_response import CustomerResponse
from openapi_client.models.customer_update import CustomerUpdate
from openapi_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "http://localhost"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure Bearer authorization: HTTPBearer
configuration = openapi_client.Configuration(
    access_token = os.environ["BEARER_TOKEN"]
)

# Enter a context with an instance of the API client
with openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.CustomersApi(api_client)
    customer_id = 56 # int | 
    customer_update = openapi_client.CustomerUpdate() # CustomerUpdate | 

    try:
        # Update Customer
        api_response = api_instance.update_customer_api_v1_customers_customer_id_put(customer_id, customer_update)
        print("The response of CustomersApi->update_customer_api_v1_customers_customer_id_put:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling CustomersApi->update_customer_api_v1_customers_customer_id_put: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **customer_id** | **int**|  | 
 **customer_update** | [**CustomerUpdate**](CustomerUpdate.md)|  | 

### Return type

[**CustomerResponse**](CustomerResponse.md)

### Authorization

[HTTPBearer](../README.md#HTTPBearer)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

