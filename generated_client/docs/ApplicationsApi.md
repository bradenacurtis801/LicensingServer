# openapi_client.ApplicationsApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_application_api_v1_applications_post**](ApplicationsApi.md#create_application_api_v1_applications_post) | **POST** /api/v1/applications/ | Create Application
[**delete_application_api_v1_applications_application_id_delete**](ApplicationsApi.md#delete_application_api_v1_applications_application_id_delete) | **DELETE** /api/v1/applications/{application_id} | Delete Application
[**get_application_api_v1_applications_application_id_get**](ApplicationsApi.md#get_application_api_v1_applications_application_id_get) | **GET** /api/v1/applications/{application_id} | Get Application
[**list_applications_api_v1_applications_get**](ApplicationsApi.md#list_applications_api_v1_applications_get) | **GET** /api/v1/applications/ | List Applications
[**update_application_api_v1_applications_application_id_put**](ApplicationsApi.md#update_application_api_v1_applications_application_id_put) | **PUT** /api/v1/applications/{application_id} | Update Application


# **create_application_api_v1_applications_post**
> ApplicationResponse create_application_api_v1_applications_post(application_create)

Create Application

Create a new application

### Example

* Bearer Authentication (HTTPBearer):

```python
import openapi_client
from openapi_client.models.application_create import ApplicationCreate
from openapi_client.models.application_response import ApplicationResponse
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
    api_instance = openapi_client.ApplicationsApi(api_client)
    application_create = openapi_client.ApplicationCreate() # ApplicationCreate | 

    try:
        # Create Application
        api_response = api_instance.create_application_api_v1_applications_post(application_create)
        print("The response of ApplicationsApi->create_application_api_v1_applications_post:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ApplicationsApi->create_application_api_v1_applications_post: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **application_create** | [**ApplicationCreate**](ApplicationCreate.md)|  | 

### Return type

[**ApplicationResponse**](ApplicationResponse.md)

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

# **delete_application_api_v1_applications_application_id_delete**
> delete_application_api_v1_applications_application_id_delete(application_id)

Delete Application

Delete an application

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
    api_instance = openapi_client.ApplicationsApi(api_client)
    application_id = 56 # int | 

    try:
        # Delete Application
        api_instance.delete_application_api_v1_applications_application_id_delete(application_id)
    except Exception as e:
        print("Exception when calling ApplicationsApi->delete_application_api_v1_applications_application_id_delete: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **application_id** | **int**|  | 

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

# **get_application_api_v1_applications_application_id_get**
> ApplicationResponse get_application_api_v1_applications_application_id_get(application_id)

Get Application

Get a specific application

### Example

* Bearer Authentication (HTTPBearer):

```python
import openapi_client
from openapi_client.models.application_response import ApplicationResponse
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
    api_instance = openapi_client.ApplicationsApi(api_client)
    application_id = 56 # int | 

    try:
        # Get Application
        api_response = api_instance.get_application_api_v1_applications_application_id_get(application_id)
        print("The response of ApplicationsApi->get_application_api_v1_applications_application_id_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ApplicationsApi->get_application_api_v1_applications_application_id_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **application_id** | **int**|  | 

### Return type

[**ApplicationResponse**](ApplicationResponse.md)

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

# **list_applications_api_v1_applications_get**
> List[ApplicationResponse] list_applications_api_v1_applications_get(skip=skip, limit=limit)

List Applications

List all applications for the authenticated user

### Example

* Bearer Authentication (HTTPBearer):

```python
import openapi_client
from openapi_client.models.application_response import ApplicationResponse
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
    api_instance = openapi_client.ApplicationsApi(api_client)
    skip = 0 # int |  (optional) (default to 0)
    limit = 100 # int |  (optional) (default to 100)

    try:
        # List Applications
        api_response = api_instance.list_applications_api_v1_applications_get(skip=skip, limit=limit)
        print("The response of ApplicationsApi->list_applications_api_v1_applications_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ApplicationsApi->list_applications_api_v1_applications_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **skip** | **int**|  | [optional] [default to 0]
 **limit** | **int**|  | [optional] [default to 100]

### Return type

[**List[ApplicationResponse]**](ApplicationResponse.md)

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

# **update_application_api_v1_applications_application_id_put**
> ApplicationResponse update_application_api_v1_applications_application_id_put(application_id, application_update)

Update Application

Update an application

### Example

* Bearer Authentication (HTTPBearer):

```python
import openapi_client
from openapi_client.models.application_response import ApplicationResponse
from openapi_client.models.application_update import ApplicationUpdate
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
    api_instance = openapi_client.ApplicationsApi(api_client)
    application_id = 56 # int | 
    application_update = openapi_client.ApplicationUpdate() # ApplicationUpdate | 

    try:
        # Update Application
        api_response = api_instance.update_application_api_v1_applications_application_id_put(application_id, application_update)
        print("The response of ApplicationsApi->update_application_api_v1_applications_application_id_put:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ApplicationsApi->update_application_api_v1_applications_application_id_put: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **application_id** | **int**|  | 
 **application_update** | [**ApplicationUpdate**](ApplicationUpdate.md)|  | 

### Return type

[**ApplicationResponse**](ApplicationResponse.md)

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

