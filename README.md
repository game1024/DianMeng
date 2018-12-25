# DianMeng BBS

www.dianmeng.us is a bbs of game development.

## Getting Started

*It's developed with falsk
*DB with mysql5.7.24-0ubuntu0.18.04.1  and redis.

### Prerequisites

* Create a new server instance.
* Push the project to github.

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

Install Python3.6.7 
```
apt-get install python3-pip
pip3 -V
```

Install Vitualenv then add the 3 lines to the bashrc.
```
pip3 install virtualenvwrapper
pip3 install --upgrade virtualenvwrapper
vim ~/.bashrc
export WORKON_HOME=$HOME/.virtualenvs
export VIRTUALENVWRAPPER_PYTHON=/usr/bin/python3.6
source /usr/local/bin/virtualenvwrapper.sh
source ~/.bashrc
```

Install Mysql
```
apt-get install mysql-server mysql-client
apt-get install libmysqld-dev
sudo mysql_secure_installation
```

Config Mysql local
```
mysql -uroot -p
use msyql
set global validate_password_policy=0;
set global validate_password_length=4;
update user set authentication_string=PASSWORD("xxxxx") where user='root';
update user set plugin="mysql_native_password";
flush privileges;
quit
```

Grant mysql remote access
```
mysql -uroot -p  
CREATE USER 'username'@'%' IDENTIFIED BY 'password';
GRANT ALL PRIVILEGES ON *.* TO 'username'@'%' WITH GRANT OPTION;
FLUSH PRIVILEGES;
vi /etc/mysql/mysql.conf.d/mysqld.cnf
comment the bind-address = 127.0.0.1
sudo service mysql restart
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

Serve flask application
```
mkvirtualenv flask-env-py3 -p python3
workon flask-env-py3
(flask-env-py3)pip3 install -r requirements.txt
app.run(host='0.0.0.0',port=5000)
```

And repeat
```
until finished
```

And repeat
```
until finished
```

And repeat
```
until finished
```

And repeat
```
until finished
```
Creating a Python Virtual Environment
```
until finished
```



And repeat

```
until finished
```

And repeat

```
until finished
```

End with an example of getting some data out of the system or using it for a little demo

## Running the tests

Explain how to run the automated tests for this system

### Break down into end to end tests

Explain what these tests test and why

```
Give an example
```

### And coding style tests

Explain what these tests test and why

```
Give an example
```

## Deployment

Add additional notes about how to deploy this on a live system

## Built With

* [Dropwizard](http://www.dropwizard.io/1.0.2/docs/) - The web framework used
* [Maven](https://maven.apache.org/) - Dependency Management
* [ROME](https://rometools.github.io/rome/) - Used to generate RSS Feeds

## Contributing

Please read [CONTRIBUTING.md](https://gist.github.com/PurpleBooth/b24679402957c63ec426) for details on our code of conduct, and the process for submitting pull requests to us.

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/your/project/tags). 

## Authors

* **Ming Zhao** - *Initial work* - [PurpleBooth](https://github.com/game102)

See also the list of [contributors](https://github.com/your/project/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Hat tip to anyone whose code was used
* Inspiration
* etc

