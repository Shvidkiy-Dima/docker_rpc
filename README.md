# Docker rpc-server

Async rpc-server for working with dock containers and docker images

## Features
* Uses websocket as a transport
* Asynchronous server-side functions
* Blocking functions are performed in threads
* Serializes docker containers and images to json or python dict
* Provides actions on docker images and containers: filter, run, stop, start, delete

## Installation

1. Clone this repository: git clone https://github.com/BorisovDima/docker_rpc.git
2. cd into docker_rpc
3. Create virtual environments: python3 -m venv venv && source venv/bin/activate
4. Install all requirements from etc/requirements.txt: pip install -r etc/requirements.txt
5. cd into app
6. launch project: python app.py
7. Go to http://localhost:8000/

## Running the tests

cd into docker_rpc/app

RUN
```
python test_api.py
```
