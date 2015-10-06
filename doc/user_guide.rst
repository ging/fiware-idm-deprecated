User and Programmers Guide
==========================

-  `Introduction <#introduction>`__

   -  `Background and Detail <#background-and-detail>`__

-  `User Guide <#user-guide>`__

   -  `Using the web portal of
      KeyRock <#using-the-web-portal-of-keyrock>`__

      -  `Logging in <#logging-in>`__
      -  `Registering an application <#registering-an-application>`__
      -  `Managing roles <#managing-roles>`__
      -  `Managing organizations <#managing-organizations>`__

-  `Programmer Guide <#programmer-guide>`__

   -  `Users <#users>`__

      -  `Get a single user <#get-a-single-user>`__
      -  `Get authenticated user <#get-authenticated-user>`__

   -  `Applications <#applications>`__

      -  `Get applications from actor (user or
         organization) <#get-applications-from-actor-user-or-organization>`__

   -  `SCIM 2.0 <#scim-20>`__

      -  `Get service provider
         configuration <#get-service-provider-configuration>`__

-  `Further information <#further-information>`__

Introduction
------------

This document describes the user and programming guide for Keyrock
Identity Management component. Here you will find the necessary steps
for use the Keyrock portal for create an account and manage it. You will
also learn about role and applications management.

Background and Detail
~~~~~~~~~~~~~~~~~~~~~

This User and Programmers Guide relates to the `Identity Management
GE <https://forge.fiware.org/plugins/mediawiki/wiki/fiware/index.php/Identity_Management_Generic_Enabler_API_Specification>`__.

User Guide
----------

Using the web portal of KeyRock
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Although every user of KeyRock will access the web portal with
individual credentials, the following description uses a test account.
In every KeyRock instance the web portal can be accessed at `**FIWARE
Account Portal** <https://account.lab.fiware.org/>`__.

Logging in
^^^^^^^^^^

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
^^^^^^^^^^^^^^^^^^^^^^^^^^

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
^^^^^^^^^^^^^^

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
^^^^^^^^^^^^^^^^^^^^^^

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
----------------

Documentation on KeyRock APIs can be found at `API Overiview
section <http://fiware-idm.readthedocs.org/en/latest/#def-api>`__

Users
~~~~~

Get a single user
^^^^^^^^^^^^^^^^^

.. raw:: html

   <pre>
     GET /users/:id
   </pre>

   <pre>
     id: 1,
     actorId: 1,
     nickName: "demo",
     displayName: "Demo user",
     email: "demo@fiware.eu",
     roles: [
       {
         id: 1,
         name: "Manager"
       },
       {
         id: 7
         name: "Ticket manager"
       }
     ],
     organizations: [
       {
          id: 1,
          actorId: 2,
          displayName: "Universidad Politecnica de Madrid",
          roles: [
            {
              id: 14,
              name: "Admin"
            }
         ]
       }
     ]
   </pre>

Get authenticated user
^^^^^^^^^^^^^^^^^^^^^^

.. raw:: html

   <pre>
     GET /user?access_token=12342134234023437
   </pre>

Applications
~~~~~~~~~~~~

Get applications from actor (user or organization)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. raw:: html

   <pre>
     GET /applications.json?actor_id=1&access_token=2YotnFZFEjr1zCsicMWpAA
   </pre>

   <pre>
     {
       id: 1,
       name: "Dummy",
       description: "fiware demo application",
       url:"http://dummy.fiware.eu/"
     }
   </pre>

SCIM 2.0
~~~~~~~~

Get service provider configuration
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. raw:: html

   <pre>
     GET /v2/ServiceProviderConfigs
   </pre>

   <pre>
     {
     "schemas":["urn:scim:schemas:core:2.0:ServiceProviderConfig"],
     "documentationUrl":"https://tools.ietf.org/html/draft-ietf-scim-core-schema-02",
     "totalUsers":"200","totalOrganizations":"50","totalResources":"250"
     }
   </pre>

Further information
-------------------

For further information on KeyRock, please refer to the step-by-step
video at `Help & Info Portal <http://help.lab.fiware.org/>`__ choosing
"Account", as `Figure 8 <#def-fig8>`__ shows.

 |image12|

.. raw:: html

   <p align="center">

Figure 8: KeyRock Screencast

.. raw:: html

   </p>

.. |image0| image:: https://raw.githubusercontent.com/ging/fiware-idm/master/doc/resources/KeyRock.png
.. |image1| image:: https://raw.githubusercontent.com/ging/fiware-idm/master/doc/resources/KeyRock_signup.png
.. |image2| image:: https://raw.githubusercontent.com/ging/fiware-idm/master/doc/resources/KeyRock_homepage.png
.. |image3| image:: https://raw.githubusercontent.com/ging/fiware-idm/master/doc/resources/KeyRock_register_app.png
.. |image4| image:: https://raw.githubusercontent.com/ging/fiware-idm/master/doc/resources/KeyRock_upload_logo.png
.. |image5| image:: https://raw.githubusercontent.com/ging/fiware-idm/master/doc/resources/KeyRock_reframe_logo.png
.. |image6| image:: https://raw.githubusercontent.com/ging/fiware-idm/master/doc/resources/KeyRock_new_role.png
.. |image7| image:: https://raw.githubusercontent.com/ging/fiware-idm/master/doc/resources/KeyRock_new_permission.png
.. |image8| image:: https://raw.githubusercontent.com/ging/fiware-idm/master/doc/resources/KeyRock_application_summary.png
.. |image9| image:: https://raw.githubusercontent.com/ging/fiware-idm/master/doc/resources/KeyRock_add_members.png
.. |image10| image:: https://raw.githubusercontent.com/ging/fiware-idm/master/doc/resources/KeyRock_create_organization.png
.. |image11| image:: https://raw.githubusercontent.com/ging/fiware-idm/master/doc/resources/KeyRock_switch_session.png
.. |image12| image:: https://raw.githubusercontent.com/ging/fiware-idm/master/doc/resources/KeyRock_screencast.png
