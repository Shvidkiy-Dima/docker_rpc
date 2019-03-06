# Docker rpc-server

# Installation

1. Clone this repository: git clone https://github.com/BorisovDima/docker_rpc.git
2. cd into docker_rpc
3. Create virtual environments: python3 -m venv venv && source venv/bin/activate
4. Install all requirements from etc/requirements.txt: pip install -r requirements.txt
5. Settings static root(docker_rpc/app/static) and server_name in etc/toornado and create s-link from etc/tornado to nginx/conf.d
6. cd into app
7. launch project: python app.py
