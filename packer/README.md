Packer with BW-Cloud
====================

#Usage

##Set credentials

You can either set the credentials direcetly in the Packer file or by exporting them as environment variables. The latter is made easy with the OpenStack RC file available in the OpenStack Dashboard and is recommended.

###Option 1: OpenStack RC file

1. Log in to the dashboard and select the project for which you want to download the OpenStack RC file.

2. Go to the Compute tab and click Access & Security.

3. Select the API Access tab and click Download OpenStack RC File. The downloaded file will be your `YOUR_CUSTOM_OPENSTACK_RC_FILE`, it consists of all necessary variables to export besides the password.

4. Source the OpenStack RC file. When you are prompted for an OpenStack password, enter your password.

    ```bash
    $ . YOUR_CUSTOM_OPENSTACK_RC_FILE
    ```

###Option 2: Variabels in Packer file

Alternatively you can set the following variables in your Packer file. You can extract this information from your OpenStack RC file. Add the following lines to your builder block. The capital worlds refere to the export variable in the OpenStack RC file:
```json
"builders":[{
  "type": "openstack",
  [...]
  "identity_endpoint": "OS_AUTH_URL",
  "region": "OS_REGION_NAME",
  "tenant_id": "OS_TENANT_ID",
  "username": "OS_USERNAME",
  "password": "OS_PASSWORD"
}]
```

##Create the OpenStack image with Packer

Build the image with your Packer file:
    
```bash
packer build ubuntu_16.04_docker.json
```
    
Relax. Installing all requirements will take some time, at the end there should be a new image at the open stack instance.

##Run Docker images on instance startup

With the created image, docker runs out of the box. With OpenStack, you can also run a docker container when you launch the instance. E.g. to automatically launch a Galaxy Instance from the [Docker Galaxy Stable](https://github.com/bgruening/docker-galaxy-stable) container, switch to the `Post-Creation` tab in the`Launch Instance` settings and enter as `Direct Input`:

```bash
#!/bin/sh
docker run -d -p 8080:80 -p 8021:21 -p 8022:22 bgruening/galaxy-stable
```

After some minutes - pulling the image will take some time - the Instance will be started and the Galaxy server up and running in Docker. Keep in mind that you have to add a security rule allowing access to the proper port (8080 in this case) from public in order to actually access the server.
