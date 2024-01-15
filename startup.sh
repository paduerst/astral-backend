#!/bin/bash

# Start up the tunnel from remote to localhost in a new Terminal window
osascript -e 'tell app "Terminal" to do script "cloudflared tunnel --url localhost:8080/"'

# Start up the localhost server in a new Terminal window
osascript -e 'tell app "Terminal" to do script "cd $HOME/Workspace/astral-backend/app && source $HOME/miniconda3/bin/activate astral_backend && node server.js"'
