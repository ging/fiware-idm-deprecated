# How to use this Dockerfile

This Dockerfile builds an image with both the front-end (Horizon) and back-end (Keystone) of the IdM installed. However, this is not enough to run the IdM. You need the following requirements:

- A

To run a Keyrock Docker container you have two options: 

- You can build your own image using the Dockerfile we provide and then run the container from it or
- You can run the container directly from the image we provide in Docker Hub.

Both options require that you have [docker](https://docs.docker.com/installation/) installed on your machine.

## Build your own image and run the container from it

You have to download the [Identity Manager's code](https://github.com/ging/fiware-idm) from GitHub and navigate to `extras/docker` directory. There, to compile your own image just run:

	sudo docker build -t idm-image .


> **Note**
> If you do not want to have to use `sudo` in this or in the next section follow [these instructions](https://docs.docker.com/installation/ubuntulinux/#create-a-docker-group).

This builds a new Docker image following the steps in `Dockerfile` and saves it in your local Docker repository with the name `idm-image`. You can check the available images in your local repository using: 

	sudo docker images


> **Note**
> If you want to know more about images and the building process you can find it in [Docker's documentation](https://docs.docker.com/userguide/dockerimages/).

Now you can run a new container from the image you have just created with:


	sudo docker run -d --name idm-container -v [host_config_file]:/opt/idm/openstack_dashboard/local/local_settings.py -v [host_db_file]:/opt/idm/keystone/keystone.db -p [host_port]:[container_port] -t idm-image


Where the different params mean: 

* -d indicates that the container runs as a daemon
* --name is the name of the new container (you can use the name you want)
* -v stablishes a relation between a local folder (in your host computer) and a container's folder. In this case it is used to pass to the container the configuration file that Horizon (the IdM front-end component) needs to work. `host_config_file` has to be the location of a local file with that configuration following the [config template](https://github.com/ging/horizon/blob/master/openstack_dashboard/local/local_settings.py.example).
* the second -v option links a local file to serve as the SQLite database. If you don't link a file from your local file system the database will be deleted every time you stop de container. Create an empty file and just pass it as an option.
* -p stablishes a relation between a local port and a container's port. You can use the port you want in `host_port` but `container_port` has to be the same that you have set in `config.app_port` in your config file. If you have set `config.https` to `true` you have to use here the https port.
* -t Allocate a pseudo-TTY, internal option for docker run.
* the last param is the name of the image


Here is an example of this command:

	sudo docker run -d --name idm -v /home/root/workspace/idm/local_settings.py:/opt/idm/openstack_dashboard/local/local_settings.py -v /home/root/workspace/idm/keystone.db:/opt/idm/keystone/keystone.db -p 5000:5000 -p 8000:8000 -t idm-image

Once the container is running you can view the console logs using: 

	sudo docker logs -f idm


To stop the container:

	sudo docker stop idm



## Run the container from the last release in Docker Hub

You can also run the container from the [image we provide](https://hub.docker.com/r/ging/idm/) in Docker Hub. In this case you have only to execute the run command. But now the image name is ging/idm:*version* where `version` is the release you want to use:

	sudo docker run -d --name idm -v [host_config_file]:/opt/idm/openstack_dashboard/local/local_settings.py -v [host_db_file]:/opt/idm/keystone/keystone.db -p 5000:5000 -p 8000:8000 -t  ging/idm

> **Note**
> If you do not specify a version you are pulling from `latest` by default.