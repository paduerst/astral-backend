ECHO OFF
START "ASTRAL Server" /D "%~dp0app" node server.js
START "ASTRAL Tunnel" /D "%~dp0tunnel" .\cloudflared.exe tunnel