# openapi_client.ActivationsApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**deactivate_machine_api_v1_activations_activation_id_delete**](ActivationsApi.md#deactivate_machine_api_v1_activations_activation_id_delete) | **DELETE** /api/v1/activations/{activation_id} | Deactivate Machine
[**get_license_activations_api_v1_activations_license_license_id_get**](ActivationsApi.md#get_license_activations_api_v1_activations_license_license_id_get) | **GET** /api/v1/activations/license/{license_id} | Get License Activations
[**list_activations_api_v1_activations_get**](ActivationsApi.md#list_activations_api_v1_activations_get) | **GET** /api/v1/activations/ | List Activations


# **deactivate_machine_api_v1_activations_activation_id_delete**
> object deactivate_machine_api_v1_activations_activation_id_delete(activation_id)

Deactivate Machine

Deactivate a machine (user must own the activation)

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
    api_instance = openapi_client.ActivationsApi(api_client)
    activation_id = 56 # int | 

    try:
        # Deactivate Machine
        api_response = api_instance.deactivate_machine_api_v1_activations_activation_id_delete(activation_id)
        print("The response of ActivationsApi->deactivate_machine_api_v1_activations_activation_id_delete:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ActivationsApi->deactivate_machine_api_v1_activations_activation_id_delete: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **activation_id** | **int**|  | 

### Return type

**object**

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

# **get_license_activations_api_v1_activations_license_license_id_get**
> List[ActivationResponse] get_license_activations_api_v1_activations_license_license_id_get(license_id)

Get License Activations

Get all activations for a specific license (user must own the license)

### Example

* Bearer Authentication (HTTPBearer):

```python
import openapi_client
from openapi_client.models.activation_response import ActivationResponse
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
    api_instance = openapi_client.ActivationsApi(api_client)
    license_id = 56 # int | 

    try:
        # Get License Activations
        api_response = api_instance.get_license_activations_api_v1_activations_license_license_id_get(license_id)
        print("The response of ActivationsApi->get_license_activations_api_v1_activations_license_license_id_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ActivationsApi->get_license_activations_api_v1_activations_license_license_id_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **license_id** | **int**|  | 

### Return type

[**List[ActivationResponse]**](ActivationResponse.md)

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

# **list_activations_api_v1_activations_get**
> List[ActivationResponse] list_activations_api_v1_activations_get(skip=skip, limit=limit)

List Activations

List activations for the authenticated user

### Example

* Bearer Authentication (HTTPBearer):

```python
import openapi_client
from openapi_client.models.activation_response import ActivationResponse
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
    api_instance = openapi_client.ActivationsApi(api_client)
    skip = 0 # int |  (optional) (default to 0)
    limit = 100 # int |  (optional) (default to 100)

    try:
        # List Activations
        api_response = api_instance.list_activations_api_v1_activations_get(skip=skip, limit=limit)
        print("The response of ActivationsApi->list_activations_api_v1_activations_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ActivationsApi->list_activations_api_v1_activations_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **skip** | **int**|  | [optional] [default to 0]
 **limit** | **int**|  | [optional] [default to 100]

### Return type

[**List[ActivationResponse]**](ActivationResponse.md)

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

