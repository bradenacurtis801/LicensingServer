# openapi_client.ValidationApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**license_heartbeat_api_v1_validation_heartbeat_post**](ValidationApi.md#license_heartbeat_api_v1_validation_heartbeat_post) | **POST** /api/v1/validation/heartbeat | License Heartbeat
[**validate_license_api_v1_validation_post**](ValidationApi.md#validate_license_api_v1_validation_post) | **POST** /api/v1/validation/ | Validate License


# **license_heartbeat_api_v1_validation_heartbeat_post**
> LicenseValidationResponse license_heartbeat_api_v1_validation_heartbeat_post(license_validation_request)

License Heartbeat

Send a heartbeat to keep activation alive (same as validation)

### Example


```python
import openapi_client
from openapi_client.models.license_validation_request import LicenseValidationRequest
from openapi_client.models.license_validation_response import LicenseValidationResponse
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
    api_instance = openapi_client.ValidationApi(api_client)
    license_validation_request = openapi_client.LicenseValidationRequest() # LicenseValidationRequest | 

    try:
        # License Heartbeat
        api_response = api_instance.license_heartbeat_api_v1_validation_heartbeat_post(license_validation_request)
        print("The response of ValidationApi->license_heartbeat_api_v1_validation_heartbeat_post:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ValidationApi->license_heartbeat_api_v1_validation_heartbeat_post: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **license_validation_request** | [**LicenseValidationRequest**](LicenseValidationRequest.md)|  | 

### Return type

[**LicenseValidationResponse**](LicenseValidationResponse.md)

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

# **validate_license_api_v1_validation_post**
> LicenseValidationResponse validate_license_api_v1_validation_post(license_validation_request)

Validate License

Validate a license key and machine combination

### Example


```python
import openapi_client
from openapi_client.models.license_validation_request import LicenseValidationRequest
from openapi_client.models.license_validation_response import LicenseValidationResponse
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
    api_instance = openapi_client.ValidationApi(api_client)
    license_validation_request = openapi_client.LicenseValidationRequest() # LicenseValidationRequest | 

    try:
        # Validate License
        api_response = api_instance.validate_license_api_v1_validation_post(license_validation_request)
        print("The response of ValidationApi->validate_license_api_v1_validation_post:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ValidationApi->validate_license_api_v1_validation_post: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **license_validation_request** | [**LicenseValidationRequest**](LicenseValidationRequest.md)|  | 

### Return type

[**LicenseValidationResponse**](LicenseValidationResponse.md)

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

