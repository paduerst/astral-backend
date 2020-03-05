const http = require('http');
const url = require('url');
const { spawn } = require('child_process');

const port = 8080;
const script = 'cam_handler.py';

const logOutput = (name) => (data) => console.log(`[${name}] ${data}`);

function run(arg1='', arg2='') {
  return new Promise((resolve, reject) => {
    const process = spawn('python', [`./${script}`, arg1, arg2]);

    const out = [];
    process.stdout.on(
      'data',
      (data) => {
        out.push(data.toString());
        logOutput('stdout')(data);
      }
    );

    const err = [];
    process.stderr.on(
      'data',
      (data) => {
        err.push(data.toString());
        logOutput('stderr')(data);
      }
    );

    process.on('exit', (code, signal) => {
      // logOutput('exit')(`${code} (${signal})`)
      if (code !== 0) {
        reject(new Error(err.join('\n')));
        return
      }
      try {
        resolve(JSON.parse(out[0]));
      } catch (e) {
        reject(e);
      }
    });
  })
}

const tryRun = async (command='', value='') => {
  try {
    const output = await run(command, value);
    // logOutput('main')(`Output: ${output} and Message: ${output.message}`);
    // process.exit(0)
    return output.message;
  } catch (e) {
    console.error('Error during script execution ', e.stack);
    process.exit(1);
  }
}

const requestListener = async function (req, res) {
  console.log(req.url);
  const q = url.parse(req.url, true).query;
  if (q.command && q.value) {
    const pyOut = await tryRun(q.command, q.value);
    res.writeHead(200, {'Content-Type': 'text/html'});
    res.write(`pyOut: ${pyOut}`);
    res.end();
  } else {
    res.writeHead(200, {'Content-Type': 'text/html'});
    res.write('Send a valid command and value next time, buddy!');
    res.end();
  }
}

const server = http.createServer(requestListener);
server.listen(port);