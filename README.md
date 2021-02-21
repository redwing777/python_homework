# UI Automation framework
```
install python
install docker(and register)
```
#### download required docker images with vnc browsers:
```
docker pull selenoid/vnc_chrome:77.0
docker pull selenoid/vnc_chrome:78.0
docker pull selenoid/video-recorder:latest-release
```
#### Install and activate virtual environment:
```
py -m pip install --user virtualenv
```
```
py -m venv env

.\env\Scripts\activate
```

#### To install packages which are required go to project directory and execute command:
```
pip install -r requirements.txt
```

### How to set non-default variables
Open constants.py where you can set:
- url
- preferred city 
- extension file path
- timeout for retries

# Tests execution possible ways:

## 1. How to run tests with test execution and webdriver on HOST without docker
#### Go to project root and execute command:
```
py.test -v --b=chrome
```
Where -b or -browser value is the name of preferred browser(Chrome, Opera, Firefox, Edge)


## 2. How to run  api tests with test execution on HOST with Selenoid:
start selenoid and selenoid-ui via docker-compose
build image
#### Go to project root and execute:
```
docker-compose up
py.test -v --b=chrome --d=1  --h=localhost --alluredir=./allure-results
```
#### after tests were finished - shutdown selenoid
```
docker-compose down
```


## 3. How to run  api tests with test execution inside container and  remote Selenoid:
start selenoid and selenoid-ui via docker-compose
build image
#### For option '--h' do not use localhost or 127.0.0.1 because container executor will send requests to himself, not to host machine.
#### Go to project root and execute:
```
docker-compose up
```
#### ^^^^^ This step - if  test executor and selenoid host are the same PC
```
docker build --no-cache . -t autotests
docker run -it  -v $(pwd):/tmp autotests bash -c "py.test -v --b=chrome --d=1  --h={IP_or_URL_of_Selenoid_host} --alluredir=/tmp/allure/allure-results"
```
192.168.3.105 in my case
#### after tests were finished - shutdown selenoid
```
docker-compose down
```

# Videos available at:
```
http://{selenoid_host}:4444/video/
or
{dir_with_dicker-compose_file}/video
```

#### how to remove all docker containers:
execute:
```
docker rmi -f $(docker images -a -q)
```
