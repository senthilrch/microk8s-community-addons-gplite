# microk8s gopaddle addon

Note: in the below, the following terms are used interchangeably to
indicate the 'gopaddle addon' on microk8s:
- gopaddle Lite addon
- gopaddle-lite addon
- gp-lite addon

## Pre-requisites

1. OS distribution: Ubuntu 18.04; MicroK8s version: 1.24; Helm version: v3.7.1

2. gopaddle Lite add-on is supported only on a single node microk8s cluster

3. System resource requirements: 8 vCPU, 32 GB RAM, 50 GB Disk

4. 'snap' tool must already be installed.

If not installed, the following steps can be used on Ubuntu 18.04:
```
sudo apt-get install snapd -y
sudo snap install core
```

5. Set the path for snap tool to be executed as a command:
```
export PATH=$PATH:/snap/bin
```

6. microk8s must already be installed and must be running.

If not installed, use the below step to install the same:
```
sudo snap install microk8s --classic --channel=1.24
```

If already installed, you may want to refresh microk8s:
```
sudo snap refresh microk8s --channel=1.24
```

7. Check and ensure that microk8s service is running:
```
sudo microk8s status --wait-ready
```

you should see output like the following:
```
microk8s is running
...
```

## Steps to install gopaddle addon for microk8s

1. Add gopaddle addon repo in microk8s:
```
sudo microk8s addons repo add gp-lite https://github.com/gopaddle-io/microk8s-community-addons-gplite.git
```

2. Check microk8s gopaddle addon is added
```
sudo microk8s status
```

Among others, you should see the following listed:
```
    ...
    gopaddle-lite        # (gp-lite) Cheapest, fastest and simplest way to modernize your applications
    ...
```

## Steps to enable gopaddle addon for microk8s

#### Step 1. Enable gopaddle addon in microk8s:
```
sudo microk8s enable gopaddle-lite
```

#### (a) Using default values:
By default, the latest gopaddle-lite version is installed, which is currently 4.2.3.

An IP address is required to access the gopaddle lite end point. When not
supplied from the command line, the default IP address is determined in the order
mentioned below:  
- If the first node in microk8s cluster is configured with an External/Public IP address, this is chosen as the IP address for the access end point
- Else, the Internal/Private IP address of the first node configured in microk8s cluster is used as the IP address for the access end point

Note: The node IP address configured in the microk8s cluster above can be determined using the 'get nodes' command of kubectl in microk8s as follows:

```
sudo microk8s kubectl  get nodes -o wide
NAME   STATUS   ROLES    AGE   VERSION                    INTERNAL-IP   EXTERNAL-IP   OS-IMAGE             KERNEL-VERSION       CONTAINER-RUNTIME
sail   Ready    <none>   37d   v1.24.0-2+59bbb3530b6769   10.245.64.9   <none>        Ubuntu 18.04.5 LTS   4.15.0-176-generic   containerd://1.5.11
```


#### Example:
```
sudo microk8s enable gopaddle-lite
Infer repository gp-lite for addon gopaddle-lite
Static IP input is not provided. External IP is not set for the microk8s node. Assuming Internal IP of the microk8s node for the gopaddle access endpoint.
...
Enabling gopaddle lite
...
"gp-lite" has been added to your repositories
...
namespace/gp-lite created
...
Waiting for the gopaddle volume to move bound. This may take a while.
...
adding label to persistentvolume
...
Waiting for the gopaddle services to move to running state. This may take a while.
...
gopaddle lite is enabled

gopaddle lite access endpoint
http://10.245.64.9:30003
```


#### (b) Using '-i' and '-v' options

You can supply \<IP Address\> and \<gopaddle version\> through command line
options during 'enable' of gopaddle lite addon in microk8s.

Usage:
```
sudo microk8s enable gopaddle-lite -i <IP Address> -v <gopaddle version>

Basic Options:
  --ip|-i      : static IP address to assign to gopaddle endpoint. This can be
                 a public or private IP address of the microk8s node
  --version|-v : gopaddle lite helm chart version (default 4.2.3)
```

If the gopaddle dashboard has to to be accessible from public network, then,
make sure that the IP address passed via '-i' option is an External/Public IP address.

<i><b>Note:</b> if '-i' and '-v' options are omitted, the default values used are as per the details already outlined under "(a) Using default values:"</i>

#### Example:
```
sudo microk8s enable gopaddle-lite -i 130.198.9.42 -v 4.2.3
```

In this case, the 'enable' command will give the below output message:
```
Infer repository gp-lite for addon gopaddle-lite
static IP of the microk8s cluster: 130.198.9.42
...
Enabling gopaddle lite
...
"gp-lite" has been added to your repositories
...
namespace/gp-lite created
...
Waiting for the gopaddle volume to move bound. This may take a while.
...
adding label to persistentvolume
...
Waiting for the gopaddle services to move to running state. This may take a while.
...
gopaddle lite is enabled

gopaddle lite access endpoint
http://130.198.9.42:30003
```
#### Important Notes:  

1. Continuous Integration (CI) capability is not supported when a managed Source Control System like GitHub.com, GitLab.com or BitBucket.com is used and the gopaddle access endpoint is not accessible from the public network.

2. To access the gopaddle dashboard from public network, make sure that this machine is configured with an External IP address as follows:

    - Either supply the External/Public IP address as the static IP address via '-i' option

    - or, make sure the first node in microk8s cluster is configured with an External/Public IP address


#### Step 2. Wait for ready state

Before you can use all the gopaddle services, they need to be in Ready state.
To check and wait until all the services move to Ready state, use the below
command:

```
sudo microk8s.kubectl wait --for=condition=ready pod -l released-by=gopaddle -n gp-lite
```

The following is a sample output when the gopaddle services are in ready state:
```
pod/rabbitmq-0 condition met
pod/influxdb-0 condition met
pod/esearch-0 condition met
pod/redis-8564f6b9fd-zqb2q condition met
pod/mongodb-0 condition met
pod/appworker-7b687d86f6-hxp8s condition met
pod/gpcore-6bc47c5c94-kq9jk condition met
pod/costmanager-564c95fcdf-x7f2t condition met
pod/clustermanager-d95cccbc-dhkl9 condition met
pod/deploymentmanager-7967f54468-qw24m condition met
pod/nodechecker-7ddfb5b556-pb9xm condition met
pod/domainmanager-7c6c6f57f7-xfn2j condition met
pod/marketplace-97bfcb68f-lnmnq condition met
pod/configmanager-5c6878bc99-8pzw7 condition met
pod/activitymanager-b7d669fb8-pcnhn condition met
pod/appscanner-677cd5799-ztrxj condition met
pod/usermanager-796bf9c8c9-f8tgg condition met
pod/cloudmanager-6c8dd7c6c5-d8xpg condition met
pod/alertmanager-77d4478976-24pgc condition met
pod/webhook-785c846b44-wxwwd condition met
pod/gateway-b768864ff-s54b2 condition met
```


#### Step 3. Access gopaddle dashboard

This is a Graphical User Interface, and can be accessed using the
above gopaddle access endpoint in a web browser of your choice.

The gopaddle lite access endpoint in the example shown above is:
```
http://10.245.64.9:30003
```

### Enabling Firewall ports

The following TCP network ports have to be enabled/opened by administrator for access:

- <b>Ports 30000 to 30006</b>: gopaddle-lite uses these network ports to provide the gopaddle-lite access endpoints.

- <b>Port 32000</b>: Service node port for Grafana dashboard on Kubernetes

- Any other network port accessed by applications launched as Kubernetes services

- Any <b>node port</b> assigned for an application deployed on microk8s


## Steps to disable gopaddle addon for microk8s

Issue the below command to disable gopaddle addon for microk8s:
```
sudo microk8s disable gopaddle-lite
```

You'll see the output as shown below:
```
Infer repository gp-lite for addon gopaddle-lite
Disabling gopaddle lite
...
namespace "gp-lite" deleted
namespace "gopaddle-servers" deleted
clusterrole.rbac.authorization.k8s.io "gopaddle:prometheus-tool-kube-state-metrics" deleted
clusterrole.rbac.authorization.k8s.io "gopaddle:prometheus-tool-server" deleted
clusterrolebinding.rbac.authorization.k8s.io "gopaddle:event-exporter-rb" deleted
clusterrolebinding.rbac.authorization.k8s.io "gopaddle:prometheus-tool-kube-state-metrics" deleted
clusterrolebinding.rbac.authorization.k8s.io "gopaddle:prometheus-tool-server" deleted
service "default-http-backend" deleted
deployment.apps "default-http-backend" deleted

removing the resourceVersion and uid in persistentvolume
persistentvolume/pvc-a6822600-e8a3-4e3c-8d83-126a941f9c5b patched
persistentvolume/pvc-90077fba-3652-4d07-abc2-dd116a314a83 patched
persistentvolume/pvc-1ab6d1ce-e8c5-47dd-8e2c-4be9289802b3 patched
persistentvolume/pvc-e10a34f8-339c-462f-94d1-ef124fa3689a patched
persistentvolume/pvc-11d6f048-864c-490c-979d-2e3987fe17c9 patched

"gp-lite" has been removed from your repositories
Disabled gopaddle lite
```

## Steps to update gopaddle addon for microk8s

At a later time, if you want to update gopaddle addon repo (that you
previously added at the time of installation of gopaddle addon for microk8s),
use the below command:

```
sudo microk8s addons repo update gp-lite
```

This results in pulling any updates done to gopaddle addon repo. If it is
already up-to-date, you will get the below output:

```
Updating repository gp-lite
Already up to date.
```

If any new updates are pulled above, in order for this to take effect, you need to
execute the following steps:  
(1) Steps to disable gopaddle addon for microk8s (described in corresponding section above)  
(2) Steps to enable gopaddle addon for microk8s (described in corresponding section above)  
 

## Steps to uninstall gopaddle addon for microk8s

Follow the below steps to uninstall gopaddle addon for microk8s:  
(1) disable gopaddle addon for microk8s (described in corresponding section above)  
(2) delete all PVs created by gopaddle (described next).

After disabling gopaddle addon for microk8s, the persistent volumes used by gopaddle
are still around. You can confirm this as follows:
```
sudo microk8s kubectl get pv
```

The following is a sample output:
```
NAME                                       CAPACITY   ACCESS MODES   RECLAIM POLICY   STATUS      CLAIM                           STORAGECLASS                  REASON   AGE
pvc-d51e8914-53a5-4085-8849-79e37b5240df   10Gi       RWO            Retain           Released    gp-lite/data-influxdb-0         microk8s-hostpath-gp-retain            41h
pvc-9131049c-68c6-4284-b56d-b8fc701620c8   10Gi       RWO            Retain           Released    gp-lite/data-mongodb-0          microk8s-hostpath-gp-retain            41h
pvc-7c12b58d-bf12-4b7e-96aa-40a0305c0748   10Gi       RWO            Retain           Released    gp-lite/data-esearch-0          microk8s-hostpath-gp-retain            41h
pvc-c758b6c1-36a5-48c7-97d4-d447052422db   10Gi       RWO            Retain           Released    gp-lite/data-rabbitmq-0         microk8s-hostpath-gp-retain            41h
pvc-a6822600-e8a3-4e3c-8d83-126a941f9c5b   10Gi       RWO            Retain           Available   gp-lite/data-influxdb-0         microk8s-hostpath-gp-retain            33h
pvc-90077fba-3652-4d07-abc2-dd116a314a83   10Gi       RWO            Retain           Available   gp-lite/data-rabbitmq-build-0   microk8s-hostpath-gp-retain            41h
pvc-1ab6d1ce-e8c5-47dd-8e2c-4be9289802b3   10Gi       RWO            Retain           Available   gp-lite/data-mongodb-0          microk8s-hostpath-gp-retain            33h
pvc-e10a34f8-339c-462f-94d1-ef124fa3689a   10Gi       RWO            Retain           Available   gp-lite/data-rabbitmq-0         microk8s-hostpath-gp-retain            33h
pvc-11d6f048-864c-490c-979d-2e3987fe17c9   10Gi       RWO            Retain           Available   gp-lite/data-esearch-0          microk8s-hostpath-gp-retain            33h
```

Use the below command to delete the persistent volumes created by gopaddle:
```
sudo microk8s kubectl delete pv -l gp-install-pv=microk8s-hostpath-gp-retain
```

The following is a sample output:
```
persistentvolume "pvc-a6822600-e8a3-4e3c-8d83-126a941f9c5b" deleted
persistentvolume "pvc-90077fba-3652-4d07-abc2-dd116a314a83" deleted
persistentvolume "pvc-1ab6d1ce-e8c5-47dd-8e2c-4be9289802b3" deleted
persistentvolume "pvc-e10a34f8-339c-462f-94d1-ef124fa3689a" deleted
persistentvolume "pvc-11d6f048-864c-490c-979d-2e3987fe17c9" deleted
```


# Helm repository for gopaddle community (lite) edition

The 'enable' script above uses the Helm repository for gopaddle community (lite)
edition. The documentation for the same is available at: https://github.com/gopaddle-io/gopaddle-lite


# Support Matrix for gp-lite

The support Matrix for gopaddle lite 4.2.3 is located at:
http://help.gopaddle.io/en/articles/6227234-support-matrix-for-gopaddle-lite-4-2-3-community-edition
 
# Help

For help related to gopaddle community (lite) edition, visit the gopaddle Help Center at:
     https://help.gopaddle.io

