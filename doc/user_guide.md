# Identity Management - KeyRock - User and Programmers Guide

- [Introduction](#)
 - [Background and Detail](#)
- [User Guide](#)
 - [Using the web portal of KeyRock](#)
  - [Logging in](#)
  - [Registering an application](#)
  - [Managing roles](#)
  - [Managing organizations](#)
- [Programmer Guide](#)
 - [Users](#)
  - [Get a single user](#)
  - [Get authenticated user](#)
 - [Applications](#)
  - [Get applications from actor (user or organization)](#)
 - [SCIM 2.0](#)
  - [Get service provider configuration](#)
- [Further information](#)

## Introduction

This document describes the user and programming guide for Keyrock Identity Management component. Here you will find the necessary steps for use the Keyrock portal for create an account and manage it. You will also learn about role and applications management.

### Background and Detail

This User and Programmers Guide relates to the [https://forge.fi-ware.org/plugins/mediawiki/wiki/fiware/index.php/Identity_Management_Generic_Enabler_API_Specification Identity Management GE].


## User Guide

### Using the web portal of KeyRock

Although every user of KeyRock will access the web portal with individual credentials, the following description uses a test account. In every KeyRock instance the web portal can be accessed at **https://account.lab.fiware.org/**.

#### Logging in

Go to "Sign in" if you heave previously created an account, otherwise "Sign up" to create a new account, [[#KeyRock Login Page|Figure 1]]. 

<br><center>[[File:KeyRock.png|600px]]   [[File:KeyRock_signup.png|600px]] </center>
<center>**Figure 1: KeyRock Login Page**</center><br>

[[#KeyRock Home Page|Figure 2]] shows the homepage after you log in successfully. 

There are two main sections, Applications and Organizations. 
In the Applications section you can register new application by clicking on "Register".

#### Registering an application

<br><center>[[File:KeyRock_homepage.png|600px]] </center>
<center>**Figure 2: KeyRock Home Page**</center><br>

In the next step you have to give the application a name, description, URL and callback URL - required by the OAuth 2.0 Protocol. 

Click on "Next" ([[#KeyRock Register Application|Figure 3]]).

<br><center>[[File:KeyRock_register_app.png|600px]] </center>
<center>**Figure 3: KeyRock Register Application**</center><br>

In the second step the application's logo will be loaded by selecting a valid file type. You have the option to re-frame the chosen image. 

Click on "Crop Image" when you complete this process and then click "Next" as shown on [[#KeyRock Edit Application Logo|Figure 4]]. 

<br><center>[[File:KeyRock_upload_logo.png|600px]] [[File:KeyRock_reframe_logo.png|600px]] </center>
<center>**Figure 4: KeyRock Edit Application Logo**</center><br>

In the third step we set up the roles and permissions of the application. You will find the two possible roles: Provider and Purchaser.

You can edit the permission for each of the roles or create new roles. Click on "New role" and write the name of role, after that click "Save".

You can configure the permissions for the new role by activating the corresponding check box. 

You are also permitted to add up new permissions by clicking on "New Permission". Here you need to enter the name of the permission, description, HTTP verb (GET, PUT, POST, DELETE) and the Path to that permission, [[#KeyRock New Roles and Permissions|Figure 5]]. 

Click "Create Permission" and "Finish" to finalize with creating the application. 

<br><center>[[File:KeyRock_new_role.png|600px]] [[File:KeyRock_new_permission.png|600px]] </center>
<center>**Figure 5: KeyRock New Roles and Permissions**</center><br>

#### Managing roles

Look at the vertical menu on the left ([[#KeyRock Add Members to Application|Figure 6]]). You went from Home to Applications. Here you can see the application you've just created. 

At the bottom you can manage the roles of the users. You can add new users on the "Add" button. 

It shows a modal where you can manage Users and Groups. You can see the users and their initially assigned roles.

Choose users and groups to add to the application, then choose their initial role. Click "Add". 

Note that you can assign roles a poteriori after the users have been added, by clicking on the roles drop down menu - below the user's icon, as shown on [[#KeyRock Add Members to Application|Figure 6]].

<br><center>[[File:KeyRock_application_summary.png|600px]] [[File:KeyRock_add_members.png|600px]]</center>
<center>**Figure 6: KeyRock Add Members to Application**</center><br>

#### Managing organizations

Next head on to the vertical menu and click "Organizations". Click "Create Organization" to register a new organization.

Add the name, choose the owner and write the description of the organization. Click "Create Organization". 

You are now redirected to the Home menu on behalf of the newly created organization. Any new application created now, will belong to the organization.

To return to the home of the user go up in the header and click on the name of the organization. Select "Switch session", [[#KeyRock Create Organization|Figure 7]].

<br><center>[[File:KeyRock_create_organization.png|600px]] [[File:KeyRock_switch_session.png|600px]]</center>
<center>**Figure 7: KeyRock Create Organization**</center><br>

## Programmer Guide

Documentation on KeyRock APIs can be found at [https://github.com/ging/fi-ware-idm/wiki KeyRock's wiki]


### Users

#### Get a single user

<pre>
  GET /users/:id
</pre>

<pre>
  id: 1,
  actorId: 1,
  nickName: "demo",
  displayName: "Demo user",
  email: "demo@fi-ware.eu",
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

#### Get authenticated user

<pre>
  GET /user?access_token=12342134234023437
</pre>

### Applications

#### Get applications from actor (user or organization)

<pre>
  GET /applications.json?actor_id=1&access_token=2YotnFZFEjr1zCsicMWpAA
</pre>

  {
    id: 1,
    name: "Dummy",
    description: "FI-WARE demo application",
    url:"http://dummy.fi-ware.eu/"
  }



### SCIM 2.0

#### Get service provider configuration

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

## Further information

For further information on KeyRock, please refer to the step-by-step video at: http://help.lab.fi-ware.org/
clicking on "Help&Info" and choosing "Account", as [[#KeyRock Screencast|Figure 8]] shows.

<br><center>[[File:KeyRock_screencast.png|800px]] </center>
<center>**Figure 3: KeyRock Screencast**</center><br>