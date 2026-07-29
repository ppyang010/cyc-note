---
Title: "telepresence"
Url: ""
Author: ""
Origin: "WizNote"
Description: ""
Tags: []
Created: "2019-06-25 10:58:26"
Cover: ""
Pinned: true
WizPinned: true
WizGuid: "237be3d6-de1a-4292-b7f3-41c4a9f9e1ae"
WizType: ""
WizLocation: "/dxy/init/"
WizDataMd5: "4e9db1a5465de717be4aa8574c19044b"
Modified: "2023-06-13 16:32:48"
WizSyncedAt: "2026-07-29 15:36:28"
---

### 1.使用kt-connect工具（推荐）

工具地址：https://alibaba.github.io/kt-connect/#/zh-cn/guide/downloads

使用方式：

获取kubectl配置文件 developer.conf，配置文件需邮件申请，领导回复后由运维提供

sudo ktctl -n dev -c developer.conf -i harbor-sf.dxy.net/k8s/kt-connect-shadow:v0.3.7 connect

搞定，具体访问方法可以参考底部的常见问题

如需访问ClusterIP有超时，可在connect命令后增加参数 --includeIps '10.0.0.0/8'

sudo ktctl -n dev -c ~/developer.conf -i harbor-sf.dxy.net/k8s/kt-connect-shadow:v0.3.7 connect

```
xxxxxxxxxx
```

1

```
sudo ktctl -n dev -c ~/developer.conf -i harbor-sf.dxy.net/k8s/kt-connect-shadow:v0.3.7 connect
```

###

---

###

### 1.安装telepresence及相关依赖软件；

| `brew cask install osxfuse`<br>`brew install datawire/blackbird/telepresence`<br>`brew install kubectl` |
| --- |

### 2.导入kubectl配置文件(配置文件需邮件申请，领导回复后由运维提供)

| `export KUBECONFIG=~/developer.conf`<br>`telepresence --deployment telepresence --namespace dev` |
| --- |

###

`telepresence --deployment telepresence --namespace test`

`export KUBECONFIG=~/developer.conftelepresence --deployment telepresence105 --namespace test   export KUBECONFIG=~/developer.conftelepresence --deployment telepresence109 --namespace dev`

###

### 3.使用以下命令连接代理服务器

| `telepresence --deployment telepresence --namespace dev``//开发环境`<br>`telepresence --deployment telepresence --namespace test``//测试环境` |
| --- |

会显示以下内容：

| `T: Warning: kubectl``1.10``.``3` `may not work correctly with cluster version``1.14``.``0` `due to the version discrepancy. See`<br>`T: https:``//kubernetes.io/docs/setup/version-skew-policy/ for more information.`<br>`T: Starting proxy with method``'vpn-tcp'``, which has the following limitations: All processes are affected, only one telepresence can`<br>`T: run per machine, and you can't use other VPNs. You may need to add cloud hosts and headless services with --also-proxy. For a full`<br>`T: list of method limitations see https:``//telepresence.io/reference/methods.html`<br>`T: Volumes are rooted at $TELEPRESENCE_ROOT. See https:``//telepresence.io/howto/volumes.html for details.`<br>`T: Starting network proxy to cluster using the existing proxy Deployment telepresence`<br>`T: No traffic is being forwarded from the remote Deployment to your local machine. You can use the --expose option to specify which`<br>`T: ports you want to forward.`<br>`T: Setup complete. Launching your command.`<br>`@developer``@kubernetes``\|bash-``3.2``$` |
| --- |

出现

| `@developer``@kubernetes``\|bash-``3.2``$` |
| --- |

命令行则可以在本地电脑访问k8s集群内容；

退出则使用exit命令断开连接即可；

### 4.注意事项：

访问集群内的应用可使用eureka上面的ip地址：{ip}:{port}
