#!/bin/bash

# start up the tunnel from remote to localhost
tilix -a session-add-right -t "ASTRAL Tunnel" --maximize -e "cloudflared tunnel"

# start up the localhost server
source $HOME/Workspace/common-scripts/bash-functions.sh
set_title "ASTRAL Server"
cd $HOME/Workspace/astral-backend/app
node server.js
