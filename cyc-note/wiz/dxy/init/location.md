---
Title: "location"
Url: ""
Author: ""
Origin: "WizNote"
Description: ""
Tags: []
Created: "2019-08-11 00:09:26"
Cover: ""
WizGuid: "ad0a9cf0-d3e3-4af7-9e7e-bc2cda7d7483"
WizType: ""
WizLocation: "/dxy/init/"
WizDataMd5: "6cb5a0180b819472d5f99501c8620c44"
Modified: "2019-08-11 00:10:17"
WizSyncedAt: "2026-07-29 15:36:28"
---

location = /japi/platform/115020002{ proxy_pass https://file.fe.host.dxy:88/japi/platform/115020002; proxy_redirect off; # 后端的Web服务器可以通过X-Forwarded-For获取用户真实IP proxy_set_header Host $host; proxy_set_header X-Real-IP $remote_addr; proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for; proxy_connect_timeout 60; proxy_read_timeout 600; send_timeout 600; }

12

1

```
location = /japi/platform/115020002{
```

2

```
            proxy_pass https://file.fe.host.dxy:88/japi/platform/115020002;
```

3

```

```

4

```
            proxy_redirect off;
```

5

```
            # 后端的Web服务器可以通过X-Forwarded-For获取用户真实IP
```

6

```
            proxy_set_header  Host  $host;
```

7

```
            proxy_set_header  X-Real-IP  $remote_addr;
```

8

```
            proxy_set_header  X-Forwarded-For  $proxy_add_x_forwarded_for;
```

9

```
            proxy_connect_timeout 60;
```

10

```
            proxy_read_timeout    600;
```

11

```
            send_timeout          600;
```

12

```
        }
```

location /japi/platform/115020002 { proxy_pass http://file.fe.host.dxy:88/japi/platform/115020002; proxy_redirect off; # 后端的Web服务器可以通过X-Forwarded-For获取用户真实IP proxy_set_header Host $host; proxy_set_header X-Real-IP $remote_addr; proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for; proxy_connect_timeout 60; proxy_read_timeout 600; send_timeout 600; }

12

1

```
 location /japi/platform/115020002 {
```

2

```
            proxy_pass http://file.fe.host.dxy:88/japi/platform/115020002;
```

3

```

```

4

```
            proxy_redirect off;
```

5

```
            # 后端的Web服务器可以通过X-Forwarded-For获取用户真实IP
```

6

```
            proxy_set_header  Host  $host;
```

7

```
            proxy_set_header  X-Real-IP  $remote_addr;
```

8

```
            proxy_set_header  X-Forwarded-For  $proxy_add_x_forwarded_for;
```

9

```
            proxy_connect_timeout 60;
```

10

```
            proxy_read_timeout    600;
```

11

```
            send_timeout          600;
```

12

```
        }
```
