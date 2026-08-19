---
Title: "公司 nginx 配置"
Url: ""
Author: ""
Origin: "WizNote"
Description: ""
Tags: []
Created: "2017-08-22 11:06:18"
Cover: ""
WizGuid: "369a602c-ead8-4b4f-8458-15f141d1bb80"
WizType: "document"
WizLocation: "/工作/浙江宇天/"
WizDataMd5: "c9105c6adb65afaae073533471300de7"
Modified: "2017-08-22 11:08:45"
WizSyncedAt: "2026-08-18 18:48:31"
---

![[attachments/7086296.png]]

nginx的配置文件中有auth_request的配置，指向了server的videoauth接口，videoauth接口根据请求的参数进行校验，若是通过校验返回200，其他情况nginx都认为校验不通过，不会接受请求，将页面指向404.html。此html写了跳转，会跳转到现网touchwap的首页。

#user nobody; worker_processes 2; error_log logs/error.log; #error_log logs/error.log notice; #error_log logs/error.log info; pid logs/nginx.pid; worker_rlimit_nofile 51200; events { use epoll; worker_connections 1024; } rtmp { server { listen 1935; chunk_size 4000; application vod { play /opt/video_files/vmspub/serverDir; } } } http { include mime.types; default_type application/octet-stream; server_names_hash_bucket_size 128; client_header_buffer_size 32k; large_client_header_buffers 4 32k; client_max_body_size 50m; limit_conn_zone $binary_remote_addr zone=perip:256k; limit_conn_log_level notice; log_format main '$remote_addr - $remote_user [$time_local] "$request" ' '$status $body_bytes_sent "$http_referer" ' '"$http_user_agent" "$http_x_forwarded_for"'; #access_log logs/access.log main; sendfile on; tcp_nopush on; #keepalive_timeout 0; keepalive_timeout 65; tcp_nodelay on; gzip on; gzip_min_length 1k; gzip_buffers 4 16k; gzip_http_version 1.0; gzip_comp_level 2; gzip_types text/plain application/x-javascript text/css application/xml; gzip_vary on; server { listen 80; server_name 192.168.101.147; #charset koi8-r; #access_log logs/host.access.log main; location / { root /opt/video_files/vmspub/serverDir; index index.html index.htm; #uwsgi_pass 127.0.0.1:9000; #include uwsgi_params; limit_rate_after 50m; limit_rate 1m; #uwsgi_param UWSGI_CHDIR /opt/nginx/vmspub/serverDir; #uwsgi_param UWSGI_SCRIPT apprun; location ~ \.flv$ { flv; } location ~ \.mp4$ { #valid_referers none blocked 192.168.3.15 192.168.3.16 192.168.3.21; #if ($invalid_referer) { # rewrite ^/ http://192.168.3.15/player/player.html; #} auth_request /auth; if ($args ~* "t=d") { add_header Content-Disposition: 'attachment;filename="download.mp4"'; add_header Content-Type: 'application/octet-stream'; } mp4; } location = /auth { proxy_pass http://192.168.101.158:9080/server/authVideo; proxy_pass_request_body off; proxy_set_header X-Original-URI $request_uri; proxy_set_header X-Original-COOKIE $http_cookie; proxy_set_header X-Original-REMOTEADDR $remote_addr; proxy_set_header X-Original-ClientType $http_client_type; } } error_page 404 403 /404.html; # redirect server error pages to the static page /50x.html # error_page 500 502 503 504 /50x.html; location = /50x.html { root html; } location ~*345x200\.jpg$ { root /opt/video_files/vmspub/serverDir; error_page 404 =200 /images/small-default.jpg; break; } location ~*480x278\.jpg$ { root /opt/video_files/vmspub/serverDir; error_page 404 =200 /images/middle-default.jpg; break; } location ~*825x480\.jpg$ { root /opt/video_files/vmspub/serverDir; error_page 404 =200 /images/big-default.jpg; break; } location ~ .*\.(gif|jpg|jpeg|png|bmp|swf|js|css)$ { #valid_referers none blocked 192.168.3.15 192.168.3.16 192.168.3.21; #if ($invalid_referer) { # rewrite ^/ http://192.168.3.15/player/player.html; #} root /opt/video_files/vmspub/serverDir; break; } location /stat { rtmp_stat all; rtmp_stat_stylesheet stat.xsl; } location /stat.xsl { root /opt/nginx/conf/; } # proxy the PHP scripts to Apache listening on 127.0.0.1:80 # #location ~ \.php$ { # proxy_pass http://127.0.0.1; #} # pass the PHP scripts to FastCGI server listening on 127.0.0.1:9000 # #location ~ \.php$ { # root html; # fastcgi_pass 127.0.0.1:9000; # fastcgi_index index.php; # fastcgi_param SCRIPT_FILENAME /scripts$fastcgi_script_name; # include fastcgi_params; #} # deny access to .htaccess files, if Apache's document root # concurs with nginx's one # #location ~ /\.ht { # deny all; #} } #server{ # listen 8000; # location /stat # { # rtmp_stat all; # rtmp_stat_stylesheet stat.xsl; # } # location /stat.xsl # { # root /opt/nginx/conf/; # } #} # another virtual host using mix of IP-, name-, and port-based configuration # #server { # listen 8000; # listen somename:8080; # server_name somename alias another.alias; # location / { # root html; # index index.html index.htm; # } #} # HTTPS server # #server { # listen 443 ssl; # server_name localhost; # ssl_certificate cert.pem; # ssl_certificate_key cert.key; # ssl_session_cache shared:SSL:1m; # ssl_session_timeout 5m; # ssl_ciphers HIGH:!aNULL:!MD5; # ssl_prefer_server_ciphers on; # location / { # root html; # index index.html index.htm; # } #} }

```
x
```

233

1

233

1

```
#user  nobody;
```

2

```
worker_processes  2;
```

3

```

```

4

```
error_log  logs/error.log;
```

5

```
#error_log  logs/error.log  notice;
```

6

```
#error_log  logs/error.log  info;
```

7

```

```

8

```
pid        logs/nginx.pid;
```

9

```

```

10

```
worker_rlimit_nofile 51200;
```

11

```

```

12

```
events {
```

13

```
    use epoll;
```

14

```
    worker_connections  1024;
```

15

```
}
```

16

```

```

17

```
rtmp {
```

18

```
    server {
```

19

```
        listen 1935;
```

20

```
        chunk_size 4000;
```

21

```
        application vod {
```

22

```
            play /opt/video_files/vmspub/serverDir;
```

23

```
        }
```

24

```
    }
```

25

```
}
```

26

```

```

27

```
http {
```

28

```
    include       mime.types;
```

29

```
    default_type  application/octet-stream;
```

30

```

```

31

```
    server_names_hash_bucket_size 128;
```

32

```
    client_header_buffer_size     32k;
```

33

```
    large_client_header_buffers   4 32k;
```

34

```

```

35

```
    client_max_body_size          50m;
```

36

```
    limit_conn_zone $binary_remote_addr zone=perip:256k;
```

37

```
    limit_conn_log_level notice;
```

38

```

```

39

```
    log_format  main  '$remote_addr - $remote_user [$time_local] "$request" '
```

40

```
                      '$status $body_bytes_sent "$http_referer" '
```

41

```
                      '"$http_user_agent" "$http_x_forwarded_for"';
```

42

```

```

43

```
    #access_log  logs/access.log  main;
```

44

```

```

45

```
    sendfile        on;
```

46

```
    tcp_nopush     on;
```

47

```

```

48

```
    #keepalive_timeout  0;
```

49

```
    keepalive_timeout  65;
```

50

```
    tcp_nodelay on;
```

51

```

```

52

```
    gzip  on;
```

53

```
    gzip_min_length 1k;
```

54

```
    gzip_buffers 4 16k;
```

55

```
    gzip_http_version 1.0;
```

56

```
    gzip_comp_level 2;
```

57

```
    gzip_types text/plain application/x-javascript text/css application/xml;
```

58

```
    gzip_vary on;
```

59

```

```

60

```
    server {
```

61

```
        listen       80;
```

62

```
        server_name  192.168.101.147;
```

63

```

```

64

```
        #charset koi8-r;
```

65

```

```

66

```
        #access_log  logs/host.access.log  main;
```

67

```

```

68

```
        location / {
```

69

```

```

70

```
            root   /opt/video_files/vmspub/serverDir;
```

71

```
            index  index.html index.htm;
```

72

```
            #uwsgi_pass 127.0.0.1:9000;
```

73

```
            #include uwsgi_params;
```

74

```
            limit_rate_after 50m;
```

75

```
            limit_rate       1m;
```

76

```
            #uwsgi_param  UWSGI_CHDIR /opt/nginx/vmspub/serverDir;
```

77

```
            #uwsgi_param  UWSGI_SCRIPT apprun;
```

78

```
            location ~ \.flv$
```

79

```
            {
```

80

```
                flv;
```

81

```
            }
```

82

```
            location ~ \.mp4$
```

83

```
            {
```

84

```
                #valid_referers none blocked 192.168.3.15 192.168.3.16 192.168.3.21;
```

85

```
                #if ($invalid_referer) {
```

86

```
                #    rewrite ^/ http://192.168.3.15/player/player.html;
```

87

```
                #}
```

88

```
        auth_request /auth;
```

89

```
                if ($args ~* "t=d")
```

90

```
                {
```

91

```
                        add_header Content-Disposition: 'attachment;filename="download.mp4"';
```

92

```
                        add_header Content-Type: 'application/octet-stream';
```

93

```
                }
```

94

```
                mp4;
```

95

```
            }
```

96

```
        location = /auth {
```

97

```
        proxy_pass http://192.168.101.158:9080/server/authVideo;
```

98

```
        proxy_pass_request_body off;
```

99

```
                proxy_set_header X-Original-URI $request_uri;
```

100

```
                proxy_set_header X-Original-COOKIE $http_cookie;
```

101

```
                proxy_set_header X-Original-REMOTEADDR $remote_addr;
```

102

```
                proxy_set_header X-Original-ClientType $http_client_type;
```

103

```

```

104

```
        }
```

105

```
        }
```

106

```

```

107

```
        error_page  404 403           /404.html;
```

108

```

```

109

```
        # redirect server error pages to the static page /50x.html
```

110

```
        #
```

111

```
        error_page   500 502 503 504  /50x.html;
```

112

```
        location = /50x.html {
```

113

```
            root   html;
```

114

```
        }
```

115

```

```

116

```
        location ~*345x200\.jpg$
```

117

```
        {
```

118

```
               root /opt/video_files/vmspub/serverDir;
```

119

```
               error_page 404 =200 /images/small-default.jpg;
```

120

```
               break;
```

121

```
        }
```

122

```

```

123

```
        location ~*480x278\.jpg$
```

124

```
        {
```

125

```
               root /opt/video_files/vmspub/serverDir;
```

126

```
               error_page 404 =200 /images/middle-default.jpg;
```

127

```
               break;
```

128

```
        }
```

129

```

```

130

```
        location ~*825x480\.jpg$
```

131

```
        {
```

132

```
               root /opt/video_files/vmspub/serverDir;
```

133

```
               error_page 404 =200 /images/big-default.jpg;
```

134

```
               break;
```

135

```
        }
```

136

```

```

137

```
        location ~ .*\.(gif|jpg|jpeg|png|bmp|swf|js|css)$
```

138

```
        {
```

139

```
                #valid_referers none blocked 192.168.3.15 192.168.3.16 192.168.3.21;
```

140

```
                #if ($invalid_referer) {
```

141

```
                #    rewrite ^/ http://192.168.3.15/player/player.html;
```

142

```
                #}
```

143

```
                root /opt/video_files/vmspub/serverDir;
```

144

```
                break;
```

145

```
        }
```

146

```

```

147

```
        location /stat
```

148

```
        {
```

149

```
            rtmp_stat all;
```

150

```
            rtmp_stat_stylesheet stat.xsl;
```

151

```
        }
```

152

```

```

153

```
        location /stat.xsl
```

154

```
        {
```

155

```
            root /opt/nginx/conf/;
```

156

```
        }
```

157

```

```

158

```
        # proxy the PHP scripts to Apache listening on 127.0.0.1:80
```

159

```
        #
```

160

```
        #location ~ \.php$ {
```

161

```
        #    proxy_pass   http://127.0.0.1;
```

162

```
        #}
```

163

```

```

164

```
        # pass the PHP scripts to FastCGI server listening on 127.0.0.1:9000
```

165

```
        #
```

166

```
        #location ~ \.php$ {
```

167

```
        #    root           html;
```

168

```
        #    fastcgi_pass   127.0.0.1:9000;
```

169

```
        #    fastcgi_index  index.php;
```

170

```
        #    fastcgi_param  SCRIPT_FILENAME  /scripts$fastcgi_script_name;
```

171

```
        #    include        fastcgi_params;
```

172

```
        #}
```

173

```

```

174

```
        # deny access to .htaccess files, if Apache's document root
```

175

```
        # concurs with nginx's one
```

176

```
        #
```

177

```
        #location ~ /\.ht {
```

178

```
        #    deny  all;
```

179

```
        #}
```

180

```
    }
```

181

```

```

182

```

```

183

```
    #server{
```

184

```
    #    listen 8000;
```

185

```
    #    location /stat
```

186

```
    #    {
```

187

```
    #        rtmp_stat all;
```

188

```
    #        rtmp_stat_stylesheet stat.xsl;
```

189

```
    #    }
```

190

```

```

191

```
    #    location /stat.xsl
```

192

```
    #    {
```

193

```
    #        root /opt/nginx/conf/;
```

194

```
    #    }
```

195

```
    #}
```

196

```
    # another virtual host using mix of IP-, name-, and port-based configuration
```

197

```
    #
```

198

```
    #server {
```

199

```
    #    listen       8000;
```

200

```
    #    listen       somename:8080;
```

201

```
    #    server_name  somename  alias  another.alias;
```

202

```

```

203

```
    #    location / {
```

204

```
    #        root   html;
```

205

```
    #        index  index.html index.htm;
```

206

```
    #    }
```

207

```
    #}
```

208

```

```

209

```

```

210

```
    # HTTPS server
```

211

```
    #
```

212

```
    #server {
```

213

```
    #    listen       443 ssl;
```

214

```
    #    server_name  localhost;
```

215

```

```

216

```
    #    ssl_certificate      cert.pem;
```

217

```
    #    ssl_certificate_key  cert.key;
```

218

```

```

219

```
    #    ssl_session_cache    shared:SSL:1m;
```

220

```
    #    ssl_session_timeout  5m;
```

221

```

```

222

```
    #    ssl_ciphers  HIGH:!aNULL:!MD5;
```

223

```
    #    ssl_prefer_server_ciphers  on;
```

224

```

```

225

```
    #    location / {
```

226

```
    #        root   html;
```

227

```
    #        index  index.html index.htm;
```

228

```
    #    }
```

229

```
    #}
```

230

```

```

231

```
}
```

232

```

```

233

```

```
