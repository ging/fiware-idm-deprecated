*******************************************
Endpoints Management Dashboard (admin-only)
*******************************************

.. contents::
   :local:
   :depth: 3


What is the Endpoints Management Dashboard
==========================================

The Endpoints Management Dashboard is a tool that helps node administrators perform CRUD operations regarding the endpoints of OpenStack services. This tool is intended for node administrators at FIWARE Lab, but it could also be used in any other cloud infrastructure. It offers the following functionalities:

- Enabling an OpenStack service for your node, by creating its user account and group and helping you create its endpoints
- Disabling an Openstack service in your node, by deleting both its user account, its endpoint group and its endpoints
- Updating the endpoints of an enabled service in your node
- Getting new credentials for the user account of a certain service in your node

.. important:: For security purposes, only admin users can access this dashboard.

User guide
==========

In this section, the different functionalities of the Endpoints Management Dashboard are covered. Remember that you can only access the Dashboard if you are a node administrator.

How to enable and disable services
----------------------------------

The following screenshot depicts the Endpoints Management Dashboard. On the left you will find the list of services which are available in the Keystone Service Catalog.

.. figure:: /resources/Endpoints_index.png
   :alt: Endpoints Management Dashboard
   :align: center

   Endpoints Management Dashboard entry point. The Dashboard has been highlighted.

The switch next to each service name will tell you whether or not the service is enabled for your node. Click on a service name to take a look at its description; endpoints and user account information will be shown too if the service is enabled for your node. If you have permissions to manage more than one region, information of all the regions will be shown.

- To enable a service, click on the switch next to its service name, and provide the endpoints for it. Both of the three interfaces (public, internal & admin are required). When you are finished, click on save to enable the service.

.. figure:: /resources/Endpoints_enable.png
   :alt: Enable service
   :align: center

   Enabling Cinder service for a certain region/regions. Input fields for endpoints interfaces immediately pop up.

- To disable a service, click on the switch next to its service name. You will be prompted with a confirmation dialog to make sure you want to proceed.

.. figure:: /resources/Endpoints_disable.png
   :alt: Disable service
   :align: center

   Disabling Nova service for a certain region/regions.

How to update a service endpoint
--------------------------------

When a service is enabled for your node, clicking on its name in the services menu on the left will show its information. To update any of the endpoints, simply change the one you need. A "Save" button will pop up to let you save your changes. Remember that you can cancel at any time.

.. figure:: /resources/Endpoints_update.png
   :alt: Update service
   :align: center

   Updating Nova endpoints. Validation of the input is performed, so as to make sure all endpoints are valid URLs.	


Managing services accounts
--------------------------

When enabling a service in your node, a user account for it is created. However, for security purposes, the password will only be showed once. If you happen to forget it, just click the "Reset password" button to request a new one. The service account user name will remain the same.

.. figure:: /resources/Endpoints_password.png
   :alt: Reset service account
   :align: center

   Use the "Reset password" button to reset the service account. The service account section has been highlighted.