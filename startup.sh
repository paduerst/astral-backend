#!/bin/bash

# start up the tunnel from remote to localhost
tilix -a session-add-right -t "ASTRAL Tunnel" -e "cloudflared tunnel"

# start up the localhost server
cd $HOME/Workspace/astral-backend/app
node server.js
