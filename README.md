# DianMeng BBS

www.dianmeng.us is a game development blog.

## Getting Started

* It's developed with Flask
* DB with mysql5.7.24 and redis.

### Prerequisites

* Create a new server instance.
* Pull the project from github.

```
Cloud server Vultr Ubuntu 18.04
Develop env python3.6.7
```

### Installing

Install essentials
```
sudo apt-get install build-essential checkinstall
sudo apt-get install libreadline-gplv2-dev libncursesw5-dev libssl-dev libsqlite3-dev tk-dev libgdbm-dev libc6-dev libbz2-dev
```

Install pip3 
```
apt-get install python3-pip
pip install --upgrade pip
pip install --upgrade setuptools
pip -V

1、pip是python的包管理工具，pip和pip3版本不同，都位于Scripts\目录下：
2、如果系统中只安装了Python2，那么就只能使用pip。
3、如果系统中只安装了Python3，那么既可以使用pip也可以使用pip3，二者是等价的。
4、如果系统中同时安装了Python2和Python3，则pip默认给Python2用，pip3指定给Python3用。
5、重要：虚拟环境中，若只存在一个python版本，可以认为在用系统中pip和pip3命令都是相同的
```

Install Vitualenv then add the 3 lines to the bashrc.
```
pip install virtualenvwrapper
pip install --upgrade virtualenvwrapper
vim ~/.bashrc             ~当前登录用户的用户目录。 登录用户是chen  cd ~   代表的就是 /home/chen/
export WORKON_HOME=$HOME/.virtualenvs
export VIRTUALENVWRAPPER_PYTHON=/usr/bin/python3.6
source /usr/local/bin/virtualenvwrapper.sh
source ~/.bashrc
```

Install Mysql
```
# 安装mysql服务
sudo apt-get install mysql-server
# 安装客户端
sudo apt install mysql-client
# 安装依赖
sudo apt install libmysqlclient-dev
# 检查状态
sudo netstat -tap | grep mysql
```

Config Mysql local
```
$ sudo su
# mysql
mysql>
mysql> select user, plugin from mysql.user;
+------------------+-----------------------+
| user             | plugin                |
+------------------+-----------------------+
| root             | auth_socket           |
| mysql.session    | mysql_native_password |
| mysql.sys        | mysql_native_password |
| debian-sys-maint | mysql_native_password |
+------------------+-----------------------+
4 rows in set (0.00 sec)
mysql> update mysql.user set authentication_string=PASSWORD('123456'), plugin='mysql_native_password' where user='root';
mysql> flush privileges;
mysql> exit
Bye
# exit
$ sudo /etc/init.d/mysql restart
$ mysql -uroot -p
```

Grant mysql remote access
```
# 修改配置文件，注释掉bind-address = 127.0.0.1
$ sudo vi /etc/mysql/mysql.conf.d/mysqld.cnf

# 保存退出，然后进入mysql服务，执行授权命令：
$ mysql -uroot -p

mysql> grant all on *.* to root@'%' identified by '123456' with grant option;
Query OK, 0 rows affected, 1 warning (0.00 sec)

mysql> flush privileges;
Query OK, 0 rows affected (0.00 sec)

mysql> exit
Bye
$ sudo /etc/init.d/mysql restart
```

Get project from GitHub.
```
mkdir -p /opt/app_server/DianMeng
cd /opt/app_server/DianMeng
apt install git
git init
git remote add origin https://github.com/game102/DianMeng.git
git pull origin master
```

If you delete something careless,you can repull
```
git reset --hard HEAD
git pull origin master
```

Create virtualenv
```
mkvirtualenv flask-env-py3 -p python3
workon flask-env-py3
(flask-env-py3)pip3 install -r requirements.txt
```

Initialize application
```
create database if not exists dianmeng default charset utf8 collate utf8_general_ci;
(flask-env-py3)python3 manage.py db init;
(flask-env-py3)python3 manage.py db migrate;
(flask-env-py3)python3 manage.py db upgrade;
(flask-env-py3)python3 manage.py create_cms_user -u zhaoming -p password -e yellowcrayon@126.com
(flask-env-py3)python3 manage.py create_role
(flask-env-py3)python3 manage.py add_user_to_role -e yellowcrayon@126.com -n "开发者"
(flask-env-py3)python3 manage.py create_front_user -e yellowcrayon@126.com -u tillow -p 12345
```

Install memcached 
```
#utils/dmcache.py (email&sms VRFY)
sudo apt-get install memcached
memcached -u root -m 32 -p 11211 -d
# memcached将会以守护程序的形式启动 memcached(-u)root用户（-d），32M内存（-m 32），监听localhost的11211端口。
sudo systemctl status memcached
#enable when system boots
sudo update-rc.d memcached enable
```

Install redis for celery
```
sudo add-apt-repository ppa:chris-lea/redis-server
sudo apt-get update
sudo apt-get install redis-server
sudo service redis-server start
#Start worker as a back ground process
(flask-env-py3)celery worker -A tasks.celery --loglevel=info -D
```

## Running the tests
```
python3 app.py
app.run(host='0.0.0.0',port=5000)
```

## Deployment

Install uWSGI
```
(flask-env-py3)apt-get install gcc
(flask-env-py3)apt-get install python3-setuptools
(flask-env-py3)apt-get install python3.6-dev
(flask-env-py3)pip install uwsgi
```

Test uWSGI
```
lsof -i:5000
kill -9 pid   xxxx
app.py=>app.run()
celery worker -A tasks.celery --loglevel=info -D
uwsgi --socket 0.0.0.0:5000 --protocol=http -w app:app
```

Config uWSGI
```
(flask-env-py3)vim /opt/app_server/DianMeng/dianmeng.ini

[uwsgi]
module = app:app
master = true
processes = 3
chdir = /opt/app_server/DianMeng
socket = /opt/app_server/DianMeng/dianmeng.sock
chmod-socket = 666      
vacuum = true		

#referring to the app.py file
#start up in master mode
#spawn 3 worker processes to serve actual requests
#socket file communication with Nginx
#can be readed and writed
#clean up the socket when the process stops

测试运行
uwsgi --ini dianmeng.ini
文件夹/opt/app_server/DianMeng/多了dianmeng.sock文件
```

Install and config Nginx
```
apt install nginx  #安装nginx

sudo vim /etc/nginx/sites-available/dianmeng

server{
	listen 80;
	server_name 149.28.80.27 www.dianmeng.us;

	location / {
		include uwsgi_params;
		uwsgi_pass unix:/opt/app_server/DianMeng/dianmeng.sock;
	}
}
```

关联sites-enabled
```
sudo ln -s /etc/nginx/sites-available/dianmeng /etc/nginx/sites-enabled
测试语法
sudo nginx -t
重启
sudo systemctl restart nginx
测试
http://149.28.80.27:80
```

Let uWSGI Detect by Systemd
```
sudo vim /etc/systemd/system/dianmeng.service

[Unit]
Description=uWSGI instance to serve DianMeng
After=syslog.target

[Service]
ExecStart=/root/.virtualenvs/flask-env-py3/bin/uwsgi --ini /opt/app_server/DianMeng/dianmeng.ini
Restart=always
KillSignal=SIGQUIT
Type=notify
StandardError=syslog
NotifyAccess=all

[Install]
WantedBy=multi-user.target
```

启动服务
```
systemctl daemon-reload 
systemctl start dianmeng
systemctl status dianmeng
```

## Acknowledgments
* Vultr Open port 25 for smtp.
