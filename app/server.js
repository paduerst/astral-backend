const express = require('express')
const url = require('url');
const { spawn } = require('child_process');

const app = express()
const port = 8080
const script = 'cam_handler.py';

function runScript(arg1, arg2, arg3) {
  return new Promise((resolve, reject) => {
    const process = spawn('python3', [`./${script}`, arg1, arg2, arg3]);

    const out = [];
    process.stdout.on(
      'data',
      (data) => {
        out.push(data.toString());
        console.log(`[stdout] ${data}`);
      }
    );

    const err = [];
    process.stderr.on(
      'data',
      (data) => {
        err.push(data.toString());
        console.log(`[stderr] ${data}`);
      }
    );

    process.on('exit', (code, signal) => {
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

const requestListener = async function (req, res) {
  console.log(req.url);
  const q = url.parse(req.url, true).query;
  if (q.command) {
    var output;
    try {
      output = await runScript(q.command, q.val1, q.val2);
    } catch (e) {
      console.error('Error during script execution ', e.stack);
      process.exit(1);
    }
    res.status(200).json(output);
  } else {
    res.json({message: 'Send a valid command next time, buddy!'});
  }
}

app.get('/', requestListener)

app.listen(port, () => console.log(`App initialized and listening on port ${port}!`))