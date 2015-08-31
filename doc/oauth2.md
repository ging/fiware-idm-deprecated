# Using the FIWARE LAB instance (OAuth2)

There is already a deployed instance of the FIWARE IdM available at https://account.lab.fiware.org/

## Register your user account

In order to start using the FIWARE IdM, [you must first register your own account](https://account.lab.fiware.org/sign_up).

## Register your application

The next step is [registering you own application](https://account.lab.fiware.org/idm/myApplications/create). The `Callback URL` attribute is a mandatory parameter used in OAuth2 authentication. The IdM provides you with a `Client ID` and a `Client Secret` which are used in OAuth2

## OAuth2 Authentication

The FIWARE IdM complies with the OAuth2 standard described in [RFC 6749](http://tools.ietf.org/html/rfc6749). Currently we support two grant types, the [Authorization Code Grant](https://tools.ietf.org/html/rfc6749#section-4.1) and the [Resource Owner Password Credentials Grant](https://tools.ietf.org/html/rfc6749#section-4.3).

### Authorization Code Grant

**Get Access Code Request**  

```http
GET /oauth2/authorize?response_type=code&client_id=1&state=xyz
&redirect_uri=https%3A%2F%2Fclient%2Eexample%2Ecom%2Fcallback_url HTTP/1.1
Host: account.lab.fiware.org
```

The `response_type` attribute is mandatory and must be set to `code`. The `client_id` attribute is the one provided by the FIWARE IdM upon application registration. The `redirect_uri` attribute must match the `Callback URL` attribute provided to the IdM within the application registration.

```http
HTTP/1.1 302 Found
Location: https://client.example.com/callback_url?code=SplxlOBeZQQYbYS6WxSbIA&state=xyz
```

**Get Access Token Request** 

```http
POST /oauth2/token HTTP/1.1
Host: account.lab.fiware.org
Authorization: Basic czZCaGRSa3F0MzpnWDFmQmF0M2JW
Content-Type: application/x-www-form-urlencoded

grant_type=authorization_code&code=SplxlOBeZQQYbYS6WxSbIA
&redirect_uri=https%3A%2F%2Fclient%2Eexample%2Ecom%2Fcallback_url
```

The `Authorization Basic` header is built with the `Client ID` and `Client Secret` credentials provided by the FIWARE IdM following the [standard](http://tools.ietf.org/html/rfc2617). So the string will be 

```
base64(client_id:client_secret)
```

The `redirect_uri` parameter must match the `Callback URL` attribute provided in the application registration.

```http
HTTP/1.1 200 OK
Content-Type: application/json;charset=UTF-8
Cache-Control: no-store
Pragma: no-cache

{
    "access_token":"2YotnFZFEjr1zCsicMWpAA",
    "token_type":"bearer",
    "expires_in":3600,
    "refresh_token":"tGzv3JOkF0XG5Qx2TlKWIA",
}
```
### Resource Owner Password Credentials Grant
```http
POST /oauth2/token HTTP/1.1
Host: account.lab.fiware.org
Authorization: Basic czZCaGRSa3F0MzpnWDFmQmF0M2JW
Content-Type: application/x-www-form-urlencoded

grant_type=password&username=demo&password=123
```

## Get user information and roles

```
GET /user?access_token=2YotnFZFEjr1zCsicMWpAA
```

```
{
  id: 1,
  displayName: "Demo user",
  email: "demo@fiware.org",
  roles: [
    {
      id: 15,
      name: "Manager"
    },
    {
      id: 7
      name: "Ticket manager"
    }
  ],
  organizations: [
    {
       id: 12,
       name: "Universidad Politecnica de Madrid",
       roles: [
         {
           id: 14,
           name: "Admin"
         }
      ]
    }
  ]
}
```