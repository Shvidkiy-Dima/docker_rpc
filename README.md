# Docker rpc-server

Async rpc-server and docker handler

# Installation

1. Clone this repository: git clone https://github.com/BorisovDima/docker_rpc.git
2. cd into docker_rpc
3. Create virtual environments: python3 -m venv venv && source venv/bin/activate
4. Install all requirements from etc/requirements.txt: pip install -r requirements.txt
5. Put static root(docker_rpc/app/static) and server_name in etc/toornado and create s-link from etc/tornado to nginx/conf.d
6. Restart nginx: service nginx restart
7. cd into app
8. launch project: python app.py
