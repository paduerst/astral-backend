const http = require('http');
const url = require('url');
const port = 8080;

const requestListener = function (req, res) {
  console.log(req.url);
  res.writeHead(200, {'Content-Type': 'text/html'});
  const q = url.parse(req.url, true).query;
  res.write(`${q.command} ${q.value}`);
  res.end();
}

const server = http.createServer(requestListener);
server.listen(port);