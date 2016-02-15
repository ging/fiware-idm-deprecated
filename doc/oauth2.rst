**************************************
Using the FIWARE LAB instance (OAuth2)
**************************************

.. contents::
   :local:
   :depth: 3


There is already a deployed instance of the FIWARE IdM available at
https://account.lab.fiware.org/

Register your user account
==========================

In order to start using the FIWARE IdM, `you must first register your
own account <https://account.lab.fiware.org/sign_up>`__.

Register your application
=========================

The next step is `registering you own
application <https://account.lab.fiware.org/idm/myApplications/create>`__.
The ``Callback URL`` attribute is a mandatory parameter used in OAuth2
authentication. The IdM provides you with a ``Client ID`` and a
``Client Secret`` which are used in OAuth2.

OAuth2 Authentication
======================

The FIWARE IdM complies with the OAuth2 standard described in `RFC
6749 <http://tools.ietf.org/html/rfc6749>`__ and supports all four grant
types defined there.

The ``Authorization Basic`` header is built with the ``Client ID`` and
``Client Secret`` credentials provided by the FIWARE IdM following the
`standard <http://tools.ietf.org/html/rfc2617>`__. So the string will be

::

    base64(client_id:client_secret)

The ``redirect_uri`` parameter must match the ``Callback URL`` attribute
provided in the application registration.

Authorization Code Grant
------------------------

The authorization code is obtained by using an authorization server (the
IdM) as an intermediary between the client (the registrered application)
and resource owner (the user). Instead of requesting authorization
directly from the resource owner, the client directs the resource owner
to an authorization server (via its user-agent as defined in
`RFC2616 <http://tools.ietf.org/html/rfc2616>`__), which in turn directs
the resource owner back to the client with the authorization code.

Authorization Request
^^^^^^^^^^^^^^^^^^^^^

.. code:: http

    GET /oauth2/authorize?response_type=code&client_id=1&state=xyz
    &redirect_uri=https%3A%2F%2Fclient%2Eexample%2Ecom%2Fcallback_url HTTP/1.1
    Host: account.lab.fiware.org

The ``response_type`` attribute is mandatory and must be set to
``code``. The ``client_id`` attribute is the one provided by the FIWARE
IdM upon application registration. The ``redirect_uri`` attribute must
match the ``Callback URL`` attribute provided to the IdM within the
application registration. ``state`` is optional and for internal use of
you application, if needed.

Authorization Response
^^^^^^^^^^^^^^^^^^^^^^

.. code:: http

    HTTP/1.1 302 Found
    Location: https://client.example.com/callback_url?code=SplxlOBeZQQYbYS6WxSbIA&state=xyz

Access Token Request
^^^^^^^^^^^^^^^^^^^^

.. code:: http

    POST /oauth2/token HTTP/1.1
    Host: account.lab.fiware.org
    Authorization: Basic czZCaGRSa3F0MzpnWDFmQmF0M2JW
    Content-Type: application/x-www-form-urlencoded

    grant_type=authorization_code&code=SplxlOBeZQQYbYS6WxSbIA
    &redirect_uri=https%3A%2F%2Fclient%2Eexample%2Ecom%2Fcallback_url

.. _access-token-response:

Access Token Response
^^^^^^^^^^^^^^^^^^^^^

.. code:: http

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

Implicit Grant
--------------

The implicit grant is a simplified authorization code flow optimized for
clients implemented in a browser using a scripting language such as
JavaScript. In the implicit flow, instead of issuing the client an
authorization code, the client is issued an access token directly (as
the result of the resource owner authorization). The grant type is
implicit, as no intermediate credentials (such as an authorization code)
are issued (and later used to obtain an access token).

Authorization Request
^^^^^^^^^^^^^^^^^^^^^

.. code:: http

    GET /oauth2/authorize?response_type=token&client_id=1&state=xyz
    &redirect_uri=https%3A%2F%2Fclient%2Eexample%2Ecom%2Fcallback_url HTTP/1.1
    Host: account.lab.fiware.org

The ``response_type`` attribute is mandatory and must be set to
``token``.

The ``client_id`` attribute is the one provided by the FIWARE
IdM upon application registration. 

The ``redirect_uri`` attribute must
match the ``Callback URL`` attribute provided to the IdM within the
application registration. 

``state`` is optional and for internal use of
you application, if needed.

Access Token Response
^^^^^^^^^^^^^^^^^^^^^

See :ref:`Authorization Code Grant <access-token-response>`

Resource Owner Password Credentials Grant
-----------------------------------------

The resource owner password credentials (i.e., username and password)
can be used directly as an authorization grant to obtain an access
token.

Access Token Request
^^^^^^^^^^^^^^^^^^^^

.. code:: http

    POST /oauth2/token HTTP/1.1
    Host: account.lab.fiware.org
    Authorization: Basic czZCaGRSa3F0MzpnWDFmQmF0M2JW
    Content-Type: application/x-www-form-urlencoded

    grant_type=password&username=demo&password=123

Access Token Response
^^^^^^^^^^^^^^^^^^^^^

See :ref:`Authorization Code Grant <access-token-response>`

Client Credentials Grant
------------------------

The client can request an access token using only its client
credentials.

Access Token Request
^^^^^^^^^^^^^^^^^^^^

.. code:: http

    POST /oauth2/token HTTP/1.1
    Host: account.lab.fiware.org
    Authorization: Basic czZCaGRSa3F0MzpnWDFmQmF0M2JW
    Content-Type: application/x-www-form-urlencoded

    grant_type=client_credentials

Access Token Response
^^^^^^^^^^^^^^^^^^^^^

See :ref:`Authorization Code Grant <access-token-response>`

Get user information and roles
==============================

.. warning:: Be aware that if you used the Client Credentials Grant to obtain the token there is no
  such thing as an 'authorizing user' because of the nature of this grant. You can still use this endpoint
  to validate the token, but the JSON (if the token is valid) will be empty.
  
Request:
::

    GET /user?access_token=2YotnFZFEjr1zCsicMWpAA

Example response:

.. code-block:: json

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
