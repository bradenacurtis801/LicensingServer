# openapi_client.LicensesApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**block_license_api_v1_licenses_license_id_block_post**](LicensesApi.md#block_license_api_v1_licenses_license_id_block_post) | **POST** /api/v1/licenses/{license_id}/block | Block License
[**create_license_api_v1_licenses_post**](LicensesApi.md#create_license_api_v1_licenses_post) | **POST** /api/v1/licenses/ | Create License
[**delete_license_api_v1_licenses_license_id_delete**](LicensesApi.md#delete_license_api_v1_licenses_license_id_delete) | **DELETE** /api/v1/licenses/{license_id} | Delete License
[**get_license_api_v1_licenses_license_id_get**](LicensesApi.md#get_license_api_v1_licenses_license_id_get) | **GET** /api/v1/licenses/{license_id} | Get License
[**list_licenses_api_v1_licenses_get**](LicensesApi.md#list_licenses_api_v1_licenses_get) | **GET** /api/v1/licenses/ | List Licenses
[**unblock_license_api_v1_licenses_license_id_unblock_post**](LicensesApi.md#unblock_license_api_v1_licenses_license_id_unblock_post) | **POST** /api/v1/licenses/{license_id}/unblock | Unblock License
[**update_license_api_v1_licenses_license_id_put**](LicensesApi.md#update_license_api_v1_licenses_license_id_put) | **PUT** /api/v1/licenses/{license_id} | Update License


# **block_license_api_v1_licenses_license_id_block_post**
> LicenseKeyResponse block_license_api_v1_licenses_license_id_block_post(license_id)

Block License

Block a license key

### Example

* Bearer Authentication (HTTPBearer):

```python
import openapi_client
from openapi_client.models.license_key_response import LicenseKeyResponse
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
    api_instance = openapi_client.LicensesApi(api_client)
    license_id = 56 # int | 

    try:
        # Block License
        api_response = api_instance.block_license_api_v1_licenses_license_id_block_post(license_id)
        print("The response of LicensesApi->block_license_api_v1_licenses_license_id_block_post:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling LicensesApi->block_license_api_v1_licenses_license_id_block_post: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **license_id** | **int**|  | 

### Return type

[**LicenseKeyResponse**](LicenseKeyResponse.md)

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

# **create_license_api_v1_licenses_post**
> LicenseKeyResponse create_license_api_v1_licenses_post(license_key_create)

Create License

Create a new license key

### Example

* Bearer Authentication (HTTPBearer):

```python
import openapi_client
from openapi_client.models.license_key_create import LicenseKeyCreate
from openapi_client.models.license_key_response import LicenseKeyResponse
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
    api_instance = openapi_client.LicensesApi(api_client)
    license_key_create = openapi_client.LicenseKeyCreate() # LicenseKeyCreate | 

    try:
        # Create License
        api_response = api_instance.create_license_api_v1_licenses_post(license_key_create)
        print("The response of LicensesApi->create_license_api_v1_licenses_post:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling LicensesApi->create_license_api_v1_licenses_post: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **license_key_create** | [**LicenseKeyCreate**](LicenseKeyCreate.md)|  | 

### Return type

[**LicenseKeyResponse**](LicenseKeyResponse.md)

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

# **delete_license_api_v1_licenses_license_id_delete**
> delete_license_api_v1_licenses_license_id_delete(license_id)

Delete License

Delete a license

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
    api_instance = openapi_client.LicensesApi(api_client)
    license_id = 56 # int | 

    try:
        # Delete License
        api_instance.delete_license_api_v1_licenses_license_id_delete(license_id)
    except Exception as e:
        print("Exception when calling LicensesApi->delete_license_api_v1_licenses_license_id_delete: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **license_id** | **int**|  | 

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

# **get_license_api_v1_licenses_license_id_get**
> LicenseKeyResponse get_license_api_v1_licenses_license_id_get(license_id)

Get License

Get a specific license

### Example

* Bearer Authentication (HTTPBearer):

```python
import openapi_client
from openapi_client.models.license_key_response import LicenseKeyResponse
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
    api_instance = openapi_client.LicensesApi(api_client)
    license_id = 56 # int | 

    try:
        # Get License
        api_response = api_instance.get_license_api_v1_licenses_license_id_get(license_id)
        print("The response of LicensesApi->get_license_api_v1_licenses_license_id_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling LicensesApi->get_license_api_v1_licenses_license_id_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **license_id** | **int**|  | 

### Return type

[**LicenseKeyResponse**](LicenseKeyResponse.md)

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

# **list_licenses_api_v1_licenses_get**
> List[LicenseKeyResponse] list_licenses_api_v1_licenses_get(skip=skip, limit=limit)

List Licenses

List all licenses for the authenticated user

### Example

* Bearer Authentication (HTTPBearer):

```python
import openapi_client
from openapi_client.models.license_key_response import LicenseKeyResponse
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
    api_instance = openapi_client.LicensesApi(api_client)
    skip = 0 # int |  (optional) (default to 0)
    limit = 100 # int |  (optional) (default to 100)

    try:
        # List Licenses
        api_response = api_instance.list_licenses_api_v1_licenses_get(skip=skip, limit=limit)
        print("The response of LicensesApi->list_licenses_api_v1_licenses_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling LicensesApi->list_licenses_api_v1_licenses_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **skip** | **int**|  | [optional] [default to 0]
 **limit** | **int**|  | [optional] [default to 100]

### Return type

[**List[LicenseKeyResponse]**](LicenseKeyResponse.md)

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

# **unblock_license_api_v1_licenses_license_id_unblock_post**
> LicenseKeyResponse unblock_license_api_v1_licenses_license_id_unblock_post(license_id)

Unblock License

Unblock a license key

### Example

* Bearer Authentication (HTTPBearer):

```python
import openapi_client
from openapi_client.models.license_key_response import LicenseKeyResponse
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
    api_instance = openapi_client.LicensesApi(api_client)
    license_id = 56 # int | 

    try:
        # Unblock License
        api_response = api_instance.unblock_license_api_v1_licenses_license_id_unblock_post(license_id)
        print("The response of LicensesApi->unblock_license_api_v1_licenses_license_id_unblock_post:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling LicensesApi->unblock_license_api_v1_licenses_license_id_unblock_post: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **license_id** | **int**|  | 

### Return type

[**LicenseKeyResponse**](LicenseKeyResponse.md)

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

# **update_license_api_v1_licenses_license_id_put**
> LicenseKeyResponse update_license_api_v1_licenses_license_id_put(license_id, license_key_update)

Update License

Update a license

### Example

* Bearer Authentication (HTTPBearer):

```python
import openapi_client
from openapi_client.models.license_key_response import LicenseKeyResponse
from openapi_client.models.license_key_update import LicenseKeyUpdate
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
    api_instance = openapi_client.LicensesApi(api_client)
    license_id = 56 # int | 
    license_key_update = openapi_client.LicenseKeyUpdate() # LicenseKeyUpdate | 

    try:
        # Update License
        api_response = api_instance.update_license_api_v1_licenses_license_id_put(license_id, license_key_update)
        print("The response of LicensesApi->update_license_api_v1_licenses_license_id_put:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling LicensesApi->update_license_api_v1_licenses_license_id_put: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **license_id** | **int**|  | 
 **license_key_update** | [**LicenseKeyUpdate**](LicenseKeyUpdate.md)|  | 

### Return type

[**LicenseKeyResponse**](LicenseKeyResponse.md)

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

