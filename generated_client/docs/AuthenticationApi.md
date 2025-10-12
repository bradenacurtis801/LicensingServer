# openapi_client.AuthenticationApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**change_password_api_v1_auth_change_password_post**](AuthenticationApi.md#change_password_api_v1_auth_change_password_post) | **POST** /api/v1/auth/change-password | Change Password
[**create_api_token_api_v1_auth_tokens_post**](AuthenticationApi.md#create_api_token_api_v1_auth_tokens_post) | **POST** /api/v1/auth/tokens | Create Api Token
[**create_user_api_v1_auth_users_post**](AuthenticationApi.md#create_user_api_v1_auth_users_post) | **POST** /api/v1/auth/users | Create User
[**delete_api_token_api_v1_auth_tokens_token_id_delete**](AuthenticationApi.md#delete_api_token_api_v1_auth_tokens_token_id_delete) | **DELETE** /api/v1/auth/tokens/{token_id} | Delete Api Token
[**get_all_users_api_v1_auth_users_get**](AuthenticationApi.md#get_all_users_api_v1_auth_users_get) | **GET** /api/v1/auth/users | Get All Users
[**get_current_user_info_api_v1_auth_me_get**](AuthenticationApi.md#get_current_user_info_api_v1_auth_me_get) | **GET** /api/v1/auth/me | Get Current User Info
[**get_user_api_v1_auth_users_user_id_get**](AuthenticationApi.md#get_user_api_v1_auth_users_user_id_get) | **GET** /api/v1/auth/users/{user_id} | Get User
[**list_api_tokens_api_v1_auth_tokens_get**](AuthenticationApi.md#list_api_tokens_api_v1_auth_tokens_get) | **GET** /api/v1/auth/tokens | List Api Tokens
[**login_api_v1_auth_login_post**](AuthenticationApi.md#login_api_v1_auth_login_post) | **POST** /api/v1/auth/login | Login
[**patch_api_token_api_v1_auth_tokens_token_id_patch**](AuthenticationApi.md#patch_api_token_api_v1_auth_tokens_token_id_patch) | **PATCH** /api/v1/auth/tokens/{token_id} | Patch Api Token
[**register_api_v1_auth_register_post**](AuthenticationApi.md#register_api_v1_auth_register_post) | **POST** /api/v1/auth/register | Register
[**update_api_token_api_v1_auth_tokens_token_id_put**](AuthenticationApi.md#update_api_token_api_v1_auth_tokens_token_id_put) | **PUT** /api/v1/auth/tokens/{token_id} | Update Api Token
[**update_user_api_v1_auth_users_user_id_put**](AuthenticationApi.md#update_user_api_v1_auth_users_user_id_put) | **PUT** /api/v1/auth/users/{user_id} | Update User
[**update_user_business_role_api_v1_auth_users_user_id_business_role_put**](AuthenticationApi.md#update_user_business_role_api_v1_auth_users_user_id_business_role_put) | **PUT** /api/v1/auth/users/{user_id}/business-role | Update User Business Role
[**update_user_system_role_api_v1_auth_users_user_id_system_role_put**](AuthenticationApi.md#update_user_system_role_api_v1_auth_users_user_id_system_role_put) | **PUT** /api/v1/auth/users/{user_id}/system-role | Update User System Role


# **change_password_api_v1_auth_change_password_post**
> object change_password_api_v1_auth_change_password_post(user_change_password)

Change Password

Change current user's password

### Example

* Bearer Authentication (HTTPBearer):

```python
import openapi_client
from openapi_client.models.user_change_password import UserChangePassword
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
    api_instance = openapi_client.AuthenticationApi(api_client)
    user_change_password = openapi_client.UserChangePassword() # UserChangePassword | 

    try:
        # Change Password
        api_response = api_instance.change_password_api_v1_auth_change_password_post(user_change_password)
        print("The response of AuthenticationApi->change_password_api_v1_auth_change_password_post:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling AuthenticationApi->change_password_api_v1_auth_change_password_post: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **user_change_password** | [**UserChangePassword**](UserChangePassword.md)|  | 

### Return type

**object**

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

# **create_api_token_api_v1_auth_tokens_post**
> APITokenCreateResponse create_api_token_api_v1_auth_tokens_post(api_token_create)

Create Api Token

Create a new API token

### Example

* Bearer Authentication (HTTPBearer):

```python
import openapi_client
from openapi_client.models.api_token_create import APITokenCreate
from openapi_client.models.api_token_create_response import APITokenCreateResponse
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
    api_instance = openapi_client.AuthenticationApi(api_client)
    api_token_create = openapi_client.APITokenCreate() # APITokenCreate | 

    try:
        # Create Api Token
        api_response = api_instance.create_api_token_api_v1_auth_tokens_post(api_token_create)
        print("The response of AuthenticationApi->create_api_token_api_v1_auth_tokens_post:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling AuthenticationApi->create_api_token_api_v1_auth_tokens_post: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **api_token_create** | [**APITokenCreate**](APITokenCreate.md)|  | 

### Return type

[**APITokenCreateResponse**](APITokenCreateResponse.md)

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

# **create_user_api_v1_auth_users_post**
> UserResponse create_user_api_v1_auth_users_post(user_create)

Create User

Create a new user (admin only)

### Example

* Bearer Authentication (HTTPBearer):

```python
import openapi_client
from openapi_client.models.user_create import UserCreate
from openapi_client.models.user_response import UserResponse
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
    api_instance = openapi_client.AuthenticationApi(api_client)
    user_create = openapi_client.UserCreate() # UserCreate | 

    try:
        # Create User
        api_response = api_instance.create_user_api_v1_auth_users_post(user_create)
        print("The response of AuthenticationApi->create_user_api_v1_auth_users_post:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling AuthenticationApi->create_user_api_v1_auth_users_post: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **user_create** | [**UserCreate**](UserCreate.md)|  | 

### Return type

[**UserResponse**](UserResponse.md)

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

# **delete_api_token_api_v1_auth_tokens_token_id_delete**
> object delete_api_token_api_v1_auth_tokens_token_id_delete(token_id)

Delete Api Token

Delete an API token

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
    api_instance = openapi_client.AuthenticationApi(api_client)
    token_id = 56 # int | 

    try:
        # Delete Api Token
        api_response = api_instance.delete_api_token_api_v1_auth_tokens_token_id_delete(token_id)
        print("The response of AuthenticationApi->delete_api_token_api_v1_auth_tokens_token_id_delete:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling AuthenticationApi->delete_api_token_api_v1_auth_tokens_token_id_delete: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **token_id** | **int**|  | 

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

# **get_all_users_api_v1_auth_users_get**
> List[UserResponse] get_all_users_api_v1_auth_users_get(skip=skip, limit=limit)

Get All Users

Get all users (admin only)

### Example

* Bearer Authentication (HTTPBearer):

```python
import openapi_client
from openapi_client.models.user_response import UserResponse
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
    api_instance = openapi_client.AuthenticationApi(api_client)
    skip = 0 # int |  (optional) (default to 0)
    limit = 100 # int |  (optional) (default to 100)

    try:
        # Get All Users
        api_response = api_instance.get_all_users_api_v1_auth_users_get(skip=skip, limit=limit)
        print("The response of AuthenticationApi->get_all_users_api_v1_auth_users_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling AuthenticationApi->get_all_users_api_v1_auth_users_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **skip** | **int**|  | [optional] [default to 0]
 **limit** | **int**|  | [optional] [default to 100]

### Return type

[**List[UserResponse]**](UserResponse.md)

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

# **get_current_user_info_api_v1_auth_me_get**
> UserResponse get_current_user_info_api_v1_auth_me_get()

Get Current User Info

Get current user information

### Example

* Bearer Authentication (HTTPBearer):

```python
import openapi_client
from openapi_client.models.user_response import UserResponse
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
    api_instance = openapi_client.AuthenticationApi(api_client)

    try:
        # Get Current User Info
        api_response = api_instance.get_current_user_info_api_v1_auth_me_get()
        print("The response of AuthenticationApi->get_current_user_info_api_v1_auth_me_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling AuthenticationApi->get_current_user_info_api_v1_auth_me_get: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**UserResponse**](UserResponse.md)

### Authorization

[HTTPBearer](../README.md#HTTPBearer)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_user_api_v1_auth_users_user_id_get**
> UserResponse get_user_api_v1_auth_users_user_id_get(user_id)

Get User

Get user by ID (admin only)

### Example

* Bearer Authentication (HTTPBearer):

```python
import openapi_client
from openapi_client.models.user_response import UserResponse
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
    api_instance = openapi_client.AuthenticationApi(api_client)
    user_id = 56 # int | 

    try:
        # Get User
        api_response = api_instance.get_user_api_v1_auth_users_user_id_get(user_id)
        print("The response of AuthenticationApi->get_user_api_v1_auth_users_user_id_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling AuthenticationApi->get_user_api_v1_auth_users_user_id_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **user_id** | **int**|  | 

### Return type

[**UserResponse**](UserResponse.md)

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

# **list_api_tokens_api_v1_auth_tokens_get**
> List[APITokenResponse] list_api_tokens_api_v1_auth_tokens_get()

List Api Tokens

List current user's API tokens

### Example

* Bearer Authentication (HTTPBearer):

```python
import openapi_client
from openapi_client.models.api_token_response import APITokenResponse
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
    api_instance = openapi_client.AuthenticationApi(api_client)

    try:
        # List Api Tokens
        api_response = api_instance.list_api_tokens_api_v1_auth_tokens_get()
        print("The response of AuthenticationApi->list_api_tokens_api_v1_auth_tokens_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling AuthenticationApi->list_api_tokens_api_v1_auth_tokens_get: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**List[APITokenResponse]**](APITokenResponse.md)

### Authorization

[HTTPBearer](../README.md#HTTPBearer)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **login_api_v1_auth_login_post**
> TokenResponse login_api_v1_auth_login_post(user_login)

Login

Login and get session token

### Example


```python
import openapi_client
from openapi_client.models.token_response import TokenResponse
from openapi_client.models.user_login import UserLogin
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
    api_instance = openapi_client.AuthenticationApi(api_client)
    user_login = openapi_client.UserLogin() # UserLogin | 

    try:
        # Login
        api_response = api_instance.login_api_v1_auth_login_post(user_login)
        print("The response of AuthenticationApi->login_api_v1_auth_login_post:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling AuthenticationApi->login_api_v1_auth_login_post: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **user_login** | [**UserLogin**](UserLogin.md)|  | 

### Return type

[**TokenResponse**](TokenResponse.md)

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

# **patch_api_token_api_v1_auth_tokens_token_id_patch**
> APITokenResponse patch_api_token_api_v1_auth_tokens_token_id_patch(token_id, api_token_update)

Patch Api Token

Partially update an API token (incremental changes)

### Example

* Bearer Authentication (HTTPBearer):

```python
import openapi_client
from openapi_client.models.api_token_response import APITokenResponse
from openapi_client.models.api_token_update import APITokenUpdate
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
    api_instance = openapi_client.AuthenticationApi(api_client)
    token_id = 56 # int | 
    api_token_update = openapi_client.APITokenUpdate() # APITokenUpdate | 

    try:
        # Patch Api Token
        api_response = api_instance.patch_api_token_api_v1_auth_tokens_token_id_patch(token_id, api_token_update)
        print("The response of AuthenticationApi->patch_api_token_api_v1_auth_tokens_token_id_patch:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling AuthenticationApi->patch_api_token_api_v1_auth_tokens_token_id_patch: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **token_id** | **int**|  | 
 **api_token_update** | [**APITokenUpdate**](APITokenUpdate.md)|  | 

### Return type

[**APITokenResponse**](APITokenResponse.md)

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

# **register_api_v1_auth_register_post**
> UserResponse register_api_v1_auth_register_post(user_create)

Register

Register a new user (public endpoint for first user, or admin-only)

### Example


```python
import openapi_client
from openapi_client.models.user_create import UserCreate
from openapi_client.models.user_response import UserResponse
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
    api_instance = openapi_client.AuthenticationApi(api_client)
    user_create = openapi_client.UserCreate() # UserCreate | 

    try:
        # Register
        api_response = api_instance.register_api_v1_auth_register_post(user_create)
        print("The response of AuthenticationApi->register_api_v1_auth_register_post:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling AuthenticationApi->register_api_v1_auth_register_post: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **user_create** | [**UserCreate**](UserCreate.md)|  | 

### Return type

[**UserResponse**](UserResponse.md)

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

# **update_api_token_api_v1_auth_tokens_token_id_put**
> APITokenResponse update_api_token_api_v1_auth_tokens_token_id_put(token_id, api_token_update)

Update Api Token

Update an API token (full update)

### Example

* Bearer Authentication (HTTPBearer):

```python
import openapi_client
from openapi_client.models.api_token_response import APITokenResponse
from openapi_client.models.api_token_update import APITokenUpdate
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
    api_instance = openapi_client.AuthenticationApi(api_client)
    token_id = 56 # int | 
    api_token_update = openapi_client.APITokenUpdate() # APITokenUpdate | 

    try:
        # Update Api Token
        api_response = api_instance.update_api_token_api_v1_auth_tokens_token_id_put(token_id, api_token_update)
        print("The response of AuthenticationApi->update_api_token_api_v1_auth_tokens_token_id_put:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling AuthenticationApi->update_api_token_api_v1_auth_tokens_token_id_put: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **token_id** | **int**|  | 
 **api_token_update** | [**APITokenUpdate**](APITokenUpdate.md)|  | 

### Return type

[**APITokenResponse**](APITokenResponse.md)

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

# **update_user_api_v1_auth_users_user_id_put**
> UserResponse update_user_api_v1_auth_users_user_id_put(user_id, user_update)

Update User

Update user (admin only)

### Example

* Bearer Authentication (HTTPBearer):

```python
import openapi_client
from openapi_client.models.user_response import UserResponse
from openapi_client.models.user_update import UserUpdate
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
    api_instance = openapi_client.AuthenticationApi(api_client)
    user_id = 56 # int | 
    user_update = openapi_client.UserUpdate() # UserUpdate | 

    try:
        # Update User
        api_response = api_instance.update_user_api_v1_auth_users_user_id_put(user_id, user_update)
        print("The response of AuthenticationApi->update_user_api_v1_auth_users_user_id_put:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling AuthenticationApi->update_user_api_v1_auth_users_user_id_put: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **user_id** | **int**|  | 
 **user_update** | [**UserUpdate**](UserUpdate.md)|  | 

### Return type

[**UserResponse**](UserResponse.md)

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

# **update_user_business_role_api_v1_auth_users_user_id_business_role_put**
> UserResponse update_user_business_role_api_v1_auth_users_user_id_business_role_put(user_id, user_business_role_update)

Update User Business Role

Update user business role (system admin only) - only USER role available

### Example

* Bearer Authentication (HTTPBearer):

```python
import openapi_client
from openapi_client.models.user_business_role_update import UserBusinessRoleUpdate
from openapi_client.models.user_response import UserResponse
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
    api_instance = openapi_client.AuthenticationApi(api_client)
    user_id = 56 # int | 
    user_business_role_update = openapi_client.UserBusinessRoleUpdate() # UserBusinessRoleUpdate | 

    try:
        # Update User Business Role
        api_response = api_instance.update_user_business_role_api_v1_auth_users_user_id_business_role_put(user_id, user_business_role_update)
        print("The response of AuthenticationApi->update_user_business_role_api_v1_auth_users_user_id_business_role_put:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling AuthenticationApi->update_user_business_role_api_v1_auth_users_user_id_business_role_put: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **user_id** | **int**|  | 
 **user_business_role_update** | [**UserBusinessRoleUpdate**](UserBusinessRoleUpdate.md)|  | 

### Return type

[**UserResponse**](UserResponse.md)

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

# **update_user_system_role_api_v1_auth_users_user_id_system_role_put**
> UserResponse update_user_system_role_api_v1_auth_users_user_id_system_role_put(user_id, user_system_role_update)

Update User System Role

Update user system role (system admin only)

### Example

* Bearer Authentication (HTTPBearer):

```python
import openapi_client
from openapi_client.models.user_response import UserResponse
from openapi_client.models.user_system_role_update import UserSystemRoleUpdate
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
    api_instance = openapi_client.AuthenticationApi(api_client)
    user_id = 56 # int | 
    user_system_role_update = openapi_client.UserSystemRoleUpdate() # UserSystemRoleUpdate | 

    try:
        # Update User System Role
        api_response = api_instance.update_user_system_role_api_v1_auth_users_user_id_system_role_put(user_id, user_system_role_update)
        print("The response of AuthenticationApi->update_user_system_role_api_v1_auth_users_user_id_system_role_put:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling AuthenticationApi->update_user_system_role_api_v1_auth_users_user_id_system_role_put: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **user_id** | **int**|  | 
 **user_system_role_update** | [**UserSystemRoleUpdate**](UserSystemRoleUpdate.md)|  | 

### Return type

[**UserResponse**](UserResponse.md)

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

