# astral-backend
Back-end for ASTRAL: Arcane System for Tabletop Roleplaying from Any Location

# Structure of ASTRAL:
- Front-end: an HTML/CSS/Javascript (JQuery? Node.js?) webapp that can be accessed at astral.duerst.me
  - Git repo can be found here: [to be added]
- HTTP requests are routed through trycloudflare which connects a public URL (randomly generated subdomain) to a localhost on the backend.
- Back-end:
  - Node.js localhost HTTP server. It handles communication between the Front-end and a Python handler script.
  - Python handler script that decides how to execute requests and listens for responses. It uses a custom library.
  - Custom Python library that does low-level camera communication.