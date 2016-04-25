**************************
User and Programmers Guide
**************************

.. contents::
   :local:
   :depth: 3


Introduction
============

This document describes the user and programming guide for Keyrock
Identity Management component. Here you will find the necessary steps
for use the Keyrock portal for create an account and manage it. You will
also learn about role and applications management.

This User and Programmers Guide relates to the `Identity Management
GE <https://forge.fiware.org/plugins/mediawiki/wiki/fiware/index.php/Identity_Management_Generic_Enabler_API_Specification>`__.


Using the web portal of KeyRock
===============================

Although every user of KeyRock will access the web portal with
individual credentials, the following description uses a test account.
In every KeyRock instance the web portal can be accessed at `**FIWARE
Account Portal** <https://account.lab.fiware.org/>`__.

Logging in
----------

Go to "Sign in" if you heave previously created an account, otherwise
"Sign up" to create a new account:

 |image0| |image1|

.. raw:: html

   <p align="center">

Figure 1: KeyRock Login Page

.. raw:: html

   </p>

`Figure 2 <#def-fig2>`__ shows the homepage after you log in
successfully.

There are two main sections, Applications and Organizations. In the
Applications section you can register new application by clicking on
"Register".

Registering an application
--------------------------

 |image2|

.. raw:: html

   <p align="center">

Figure 2: KeyRock Home Page

.. raw:: html

   </p>

In the next step you have to give the application a name, description,
URL and callback URL - required by the OAuth 2.0 Protocol.

Click on "Next" (`Figure 3 <#def-fig3>`__).

 |image3|

.. raw:: html

   <p align="center">

Figure 3: KeyRock Register Application

.. raw:: html

   </p>

In the second step the application's logo will be loaded by selecting a
valid file type. You have the option to re-frame the chosen image.

Click on "Crop Image" when you complete this process and then click
"Next" as shown on `Figure 4 <#def-fig4>`__.

 |image4| |image5|

.. raw:: html

   <p align="center">

Figure 4: KeyRock Edit Application Logo

.. raw:: html

   </p>

In the third step we set up the roles and permissions of the
application. You will find the two possible roles: Provider and
Purchaser.

You can edit the permission for each of the roles or create new roles.
Click on "New role" and write the name of role, after that click "Save".

You can configure the permissions for the new role by activating the
corresponding check box.

You are also permitted to add up new permissions by clicking on "New
Permission". Here you need to enter the name of the permission,
description, HTTP verb (GET, PUT, POST, DELETE) and the Path to that
permission, `Figure 5 <#def-fig5>`__.

Click "Create Permission" and "Finish" to finalize with creating the
application.

 |image6| |image7|

.. raw:: html

   <p align="center">

Figure 5: KeyRock New Roles and Permissions

.. raw:: html

   </p>

Managing roles
--------------

Look at the vertical menu on the left (`Figure 6 <#def-fig6>`__). You
went from Home to Applications. Here you can see the application you've
just created.

At the bottom you can manage the roles of the users. You can add new
users on the "Add" button.

It shows a modal where you can manage Users and Groups. You can see the
users and their initially assigned roles.

Choose users and groups to add to the application, then choose their
initial role. Click "Add".

Note that you can assign roles after the users have been added, by
clicking on the roles drop down menu - below the user's icon, as shown
on `Figure 6 <#def-fig6>`__.

 |image8| |image9|

.. raw:: html

   <p align="center">

Figure 6: KeyRock Add Members to Application

.. raw:: html

   </p>

Managing organizations
----------------------

Next head on to the vertical menu and click "Organizations". Click
"Create Organization" to register a new organization.

Add the name, choose the owner and write the description of the
organization. Click "Create Organization".

You are now redirected to the Home menu on behalf of the newly created
organization. Any new application created now, will belong to the
organization.

To return to the home of the user go up in the header and click on the
name of the organization. Select "Switch session", `Figure
7 <#def-fig7>`__.

 |image10| |image11|

.. raw:: html

   <p align="center">

Figure 7: KeyRock Create Organization

.. raw:: html

   </p>

Programmer Guide
================

Documentation on KeyRock APIs can be found at :ref:`API Overiview
section <api>`

Users
-----

Get a single user
^^^^^^^^^^^^^^^^^

Request:

.. code-block:: html

  GET /users/:id

Example response:

.. code-block:: json

  {
    "id": 1,
    "actorId": 1,
    "nickName": "demo",
    "displayName": "Demo user",
    "email": "demo@fiware.eu",
    "roles": [
     {
       "id": 1,
       "name": "Manager"
     },
     {
       "id": 7
       "name": "Ticket manager"
     }
    ],
    "organizations": [
     {
        "id": 1,
        "actorId": 2,
        "displayName": "Universidad Politecnica de Madrid",
        "roles": [
          {
            "id": 14,
            "name": "Admin"
          }
       ]
     }
    ]
  }

Get authenticated user
^^^^^^^^^^^^^^^^^^^^^^

Request:

.. code-block:: html

     GET /user?access_token=12342134234023437

Applications
------------

Get applications from actor (user or organization)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Request:

.. code-block:: html

  GET /applications.json?actor_id=1&access_token=2YotnFZFEjr1zCsicMWpAA

Example response:

.. code-block:: json

  {
    "id": 1,
    "name": "Dummy",
    "description": "fiware demo application",
    "url": "http://dummy.fiware.eu/"
  }

SCIM 2.0
---------

Documentation on KeyRock APIs can be found at :ref:`API Overiview section <api>`. We provide bellow an example of API call, to retrieve the service provider documentation.

Get service provider configuration
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Request:

.. code-block:: html

  GET /v2/ServiceProviderConfigs

Example response:

.. code-block:: json

  {
    "schemas": [
      "urn:scim:schemas:core:2.0:ServiceProviderConfig"
    ],
    "documentationUrl": "https://tools.ietf.org/html/draft-ietf-scim-core-schema-02",
    "totalUsers": "200",
    "totalOrganizations": "50",
    "totalResources": "250"
  }

Further information
===================

For further information on KeyRock, please refer to the step-by-step
video at `Help & Info Portal <http://help.lab.fiware.org/>`__ choosing
"Account", as `Figure 8 <#def-fig8>`__ shows.

 |image12|

.. raw:: html

   <p align="center">

Figure 8: KeyRock Screencast

.. raw:: html

   </p>

.. |image0| image:: /resources/KeyRock.png
.. |image1| image:: /resources/KeyRock_signup.png
.. |image2| image:: /resources/KeyRock_homepage.png
.. |image3| image:: /resources/KeyRock_register_app.png
.. |image4| image:: /resources/KeyRock_upload_logo.png
.. |image5| image:: /resources/KeyRock_reframe_logo.png
.. |image6| image:: /resources/KeyRock_new_role.png
.. |image7| image:: /resources/KeyRock_new_permission.png
.. |image8| image:: /resources/KeyRock_application_summary.png
.. |image9| image:: /resources/KeyRock_add_members.png
.. |image10| image:: /resources/KeyRock_create_organization.png
.. |image11| image:: /resources/KeyRock_switch_session.png
.. |image12| image:: /resources/KeyRock_screencast.png
