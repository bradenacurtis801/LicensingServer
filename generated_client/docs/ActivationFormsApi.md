# openapi_client.ActivationFormsApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**complete_activation_form_api_v1_activation_forms_complete_post**](ActivationFormsApi.md#complete_activation_form_api_v1_activation_forms_complete_post) | **POST** /api/v1/activation-forms/complete | Complete Activation Form
[**create_activation_form_api_v1_activation_forms_post**](ActivationFormsApi.md#create_activation_form_api_v1_activation_forms_post) | **POST** /api/v1/activation-forms/ | Create Activation Form
[**generate_offline_codes_api_v1_activation_forms_offline_codes_post**](ActivationFormsApi.md#generate_offline_codes_api_v1_activation_forms_offline_codes_post) | **POST** /api/v1/activation-forms/offline-codes | Generate Offline Codes
[**get_activation_form_api_v1_activation_forms_form_id_get**](ActivationFormsApi.md#get_activation_form_api_v1_activation_forms_form_id_get) | **GET** /api/v1/activation-forms/{form_id} | Get Activation Form
[**list_activation_forms_api_v1_activation_forms_get**](ActivationFormsApi.md#list_activation_forms_api_v1_activation_forms_get) | **GET** /api/v1/activation-forms/ | List Activation Forms


# **complete_activation_form_api_v1_activation_forms_complete_post**
> ActivationFormResponse complete_activation_form_api_v1_activation_forms_complete_post(activation_form_complete)

Complete Activation Form

Complete an activation form with activation code

### Example


```python
import openapi_client
from openapi_client.models.activation_form_complete import ActivationFormComplete
from openapi_client.models.activation_form_response import ActivationFormResponse
from openapi_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.ActivationFormsApi(api_client)
    activation_form_complete = openapi_client.ActivationFormComplete() # ActivationFormComplete | 

    try:
        # Complete Activation Form
        api_response = api_instance.complete_activation_form_api_v1_activation_forms_complete_post(activation_form_complete)
        print("The response of ActivationFormsApi->complete_activation_form_api_v1_activation_forms_complete_post:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ActivationFormsApi->complete_activation_form_api_v1_activation_forms_complete_post: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **activation_form_complete** | [**ActivationFormComplete**](ActivationFormComplete.md)|  | 

### Return type

[**ActivationFormResponse**](ActivationFormResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_activation_form_api_v1_activation_forms_post**
> ActivationFormResponse create_activation_form_api_v1_activation_forms_post(activation_form_create)

Create Activation Form

Create a new activation form request (for offline computers)

### Example


```python
import openapi_client
from openapi_client.models.activation_form_create import ActivationFormCreate
from openapi_client.models.activation_form_response import ActivationFormResponse
from openapi_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.ActivationFormsApi(api_client)
    activation_form_create = openapi_client.ActivationFormCreate() # ActivationFormCreate | 

    try:
        # Create Activation Form
        api_response = api_instance.create_activation_form_api_v1_activation_forms_post(activation_form_create)
        print("The response of ActivationFormsApi->create_activation_form_api_v1_activation_forms_post:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ActivationFormsApi->create_activation_form_api_v1_activation_forms_post: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **activation_form_create** | [**ActivationFormCreate**](ActivationFormCreate.md)|  | 

### Return type

[**ActivationFormResponse**](ActivationFormResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **generate_offline_codes_api_v1_activation_forms_offline_codes_post**
> List[OfflineActivationCodeResponse] generate_offline_codes_api_v1_activation_forms_offline_codes_post(offline_activation_code_create)

Generate Offline Codes

Generate offline activation codes for a license

### Example


```python
import openapi_client
from openapi_client.models.offline_activation_code_create import OfflineActivationCodeCreate
from openapi_client.models.offline_activation_code_response import OfflineActivationCodeResponse
from openapi_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.ActivationFormsApi(api_client)
    offline_activation_code_create = openapi_client.OfflineActivationCodeCreate() # OfflineActivationCodeCreate | 

    try:
        # Generate Offline Codes
        api_response = api_instance.generate_offline_codes_api_v1_activation_forms_offline_codes_post(offline_activation_code_create)
        print("The response of ActivationFormsApi->generate_offline_codes_api_v1_activation_forms_offline_codes_post:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ActivationFormsApi->generate_offline_codes_api_v1_activation_forms_offline_codes_post: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **offline_activation_code_create** | [**OfflineActivationCodeCreate**](OfflineActivationCodeCreate.md)|  | 

### Return type

[**List[OfflineActivationCodeResponse]**](OfflineActivationCodeResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_activation_form_api_v1_activation_forms_form_id_get**
> ActivationFormResponse get_activation_form_api_v1_activation_forms_form_id_get(form_id)

Get Activation Form

Get a specific activation form

### Example


```python
import openapi_client
from openapi_client.models.activation_form_response import ActivationFormResponse
from openapi_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.ActivationFormsApi(api_client)
    form_id = 56 # int | 

    try:
        # Get Activation Form
        api_response = api_instance.get_activation_form_api_v1_activation_forms_form_id_get(form_id)
        print("The response of ActivationFormsApi->get_activation_form_api_v1_activation_forms_form_id_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ActivationFormsApi->get_activation_form_api_v1_activation_forms_form_id_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **form_id** | **int**|  | 

### Return type

[**ActivationFormResponse**](ActivationFormResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_activation_forms_api_v1_activation_forms_get**
> List[ActivationFormResponse] list_activation_forms_api_v1_activation_forms_get(skip=skip, limit=limit)

List Activation Forms

List all activation forms

### Example


```python
import openapi_client
from openapi_client.models.activation_form_response import ActivationFormResponse
from openapi_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.ActivationFormsApi(api_client)
    skip = 0 # int |  (optional) (default to 0)
    limit = 100 # int |  (optional) (default to 100)

    try:
        # List Activation Forms
        api_response = api_instance.list_activation_forms_api_v1_activation_forms_get(skip=skip, limit=limit)
        print("The response of ActivationFormsApi->list_activation_forms_api_v1_activation_forms_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ActivationFormsApi->list_activation_forms_api_v1_activation_forms_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **skip** | **int**|  | [optional] [default to 0]
 **limit** | **int**|  | [optional] [default to 100]

### Return type

[**List[ActivationFormResponse]**](ActivationFormResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

