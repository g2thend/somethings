# docker 部署openvpn flask

## 部署mysql

首先创建docker 网络,这样两个容器可在网络上互通,flask 容器可以使用mysql的端口

```bash
#####

$ docker network create  flask-net


#启动数据库
docker run -d   --restart=always --name  vpnsql  --net  flask-net  -p 3306:3306  -v /home/data/openvpn-mysql-data:/var/lib/mysql/  -e MYSQL_ROOT_PASSWORD=Data   mysql:5.6

#新建用户授权并导入数据库
mysql -uroot   -pData
grant  all  privileges on *.* to 'sight'@'%'   identified by "123456" ;
flush privileges ;

#进去容器导入数据库
mysql -usight  -p123456  <  open-vpn.sql 


#########################################
#########################################
##注意,openvpn验证用户连接后,会使用数据库自带的now() 函数写入当前的系统时间,需要修改时间为东八区北京时间,否则flask 页面显示的日志时间异常
#连接数据库修改
> set global time_zone = '+8:00'; ##修改mysql全局时区为北京时间，即我们所在的东8区
> set time_zone = '+8:00'; ##修改当前会话时区
> flush privileges; #立即生效



#数据库配置文件修改
# vim /etc/my.cnf ##在[mysqld]区域中加上
default-time_zone = '+8:00'
```



如果更改了连接数据库的账号和密码,需要改变flask连接数据库的配置:

```bash 
(flask-vpn) [root@mini-install openvpn]# ll
total 20
drwxr-xr-x. 2 root root   67 May 29 11:19 download
-rw-r--r--. 1 root root 9000 Jun  1 11:29 main.py
-rw-r--r--. 1 root root  186 May 29 11:19 requirement.txt
drwxr-xr-x. 2 root root 4096 May 29 11:19 static
drwxr-xr-x. 2 root root  145 Jun  1 11:29 templates

(flask-vpn) [root@mini-install openvpn]# vim  main.py
#app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://sight:123456@192.168.190.147/open-vpn"    ##这个是本地测试的IP地址
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://sight:123456@vpnsql/open-vpn"        ##容器部署时vpnsql 是数据库的容器名称

##修改sight:123456    账号:密码
```



## flask  镜像生成

https://github.com/tiangolo/uwsgi-nginx-flask-docker

将自己的flask源码打包生成镜像

```bash
#目录结构
(flask-vpn) [root@mini-install flask-docker]# tree  -L 2
.
├── Dockerfile
└── openvpn
    ├── download
    ├── main.py
    ├── requirement.txt
    ├── static
    └── templates

##Dockerfile 
FROM tiangolo/uwsgi-nginx-flask:python3.8
COPY ./openvpn  /app
RUN pip install -r /app/requirement.txt -i  https://pypi.tuna.tsinghua.edu.cn/simple some-package --no-cache-dir



##构建镜像
#注意.构建需要在有网环境下下载需要安装的Python 包,
docker build -t  web-openvpn  . 


##或者在有镜像的基础上修改dockerfile
#比如:

vim  Dockerfile 
FROM web-openvpn
##web-openvpn  是已经存在的镜像
COPY ./openvpn  /app
##openvpn  是已经修改过得flask 源码



##构建镜像
docker build -t  web-openvpn-v1  . 


##镜像导入到服务器内
##启动容器
docker run -d   --restart=always  -p 8080:80  --name  web-openvpn --net  flask-net   web-openvpn

##访问:
ip:8080 
```





