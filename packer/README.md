Packer with BW-Cloud
====================

##Usage

1. Source your OpenStack RC-file. When asked to, enter your passsword. You can download it in the OpenStack dashboard at "Access & Security->API Access".

    ```source YOUR_CUSTOM_OPENSTACK_RC_FILE```

2. Build the image.
    
    ```packer build ubuntu_16.04_docker.json````
    
3. Wait. Installing all requirements will take some time, at the end there should be a new image at the open stack instance.
