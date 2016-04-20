# How to use this Dockerfile

This Dockerfile builds an image with both the front-end (Horizon) and back-end (Keystone) of the IdM installed.

To run a Keyrock Docker container you have two options: 

- You can build your own image using the Dockerfile we provide and then run the container from it, as described [here](#build-your-own-image-and-run-the-container-from-it), or
- You can run the container directly from the image we provide in Docker Hub, as described [here](#run-the-container-from-the-last-release-in-docker-hub).

Both options require that you have [Docker](https://docs.docker.com/installation/) installed on your machine.

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

	sudo docker run -d --name idm-container -p [host_port]:[container_port] -t idm-image

Where the different params mean:

* `-d` indicates that the container runs as a daemon.
* `--name` is the name of the new container (you can use the name you want)
* `-p` stablishes a relation between a local port and a container's port. You can use the port you want in `host_port`, but `container_port` must be either `5000` or `8000`, since these are the only ports in the container which will be exposed.
* `-t` allocates a pseudo-TTY, internal option for *docker run*.
* the last param is the name of the image.

Here is an example of this command:

	sudo docker run -d --name idm -p 8000:8000 -p 5000:5000 -t idm-image

Once the container is running you can view the console logs using: 

	sudo docker logs -f idm

To stop the container:

	sudo docker stop idm
	
And to start it back again:

	sudo docker start idm

## Run the container from the last release in Docker Hub

You can also run the container from the [image we provide](https://hub.docker.com/r/fiware/idm/) in Docker Hub. In this case you have only to execute the `run` command. But now the image name is fiware/idm:*version* where `version` is the release you want to use:

	sudo docker run -d --name idm -p 8000:8000 -p 5000:5000 -t  fiware/idm

> **Note**
> If you do not specify a version you are pulling from `latest` by default.

# Default settings included in the Image
The image includes the following settings as defaults, but you can change any of them by accessing the container (see [this](#volumes)) or changing the Dockerfile:

| Setting       | Value  |
|:-------------:|:------:|
| idm user      | `idm`  |
| idm password  | `idm`  |
| Horizon port  | `8000` |
| Keystone port | `5000` |

# Volumes
Both `keystone` and `horizon` directories can be accessed through two mounted Docker data volumes. You just need to navigate to the certain mount point, which changes every time the container is created, but can be shown running the following (use the name of your container instead of `idm-container`:

	sudo docker inspect idm-container

The `Mounts` section contains the mount points of the volumes, right after the `Source` key. For example:
	
```JSON
"Mounts": [
       	{
       	"Name": "e7bfca8928745b25f1101e97b0e9ec6c43a7e53e101b3817de97106eebc8d504",
       	"Source": "/var/lib/docker/volumes/e7bfca8928745b25f1101e97b0e9ec6c43a7e53e101b3817de97106eebc8d504/_data",
        "Destination": "/keystone",
        "Driver": "local",
        "Mode": "",
        "RW": true
        },
       	{
        "Name": "0e3816196a43b14a82bbe922dd1fce7aea8f71640b38b036b51e1869f82c5571",
        "Source": "/var/lib/docker/volumes/0e3816196a43b14a82bbe922dd1fce7aea8f71640b38b036b51e1869f82c5571/_data",
        "Destination": "/horizon",
        "Driver": "local",
        "Mode": "",
        "RW": true
        }
]
```

You can learn more about Docker volumes [here](https://docs.docker.com/engine/userguide/dockervolumes/).
