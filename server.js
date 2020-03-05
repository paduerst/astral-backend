const express = require('express')
const app = express()
const port = 8080

app.get('/', (req, res) => res.send(`Hello World! URL: ${req.url}`))
app.get('/:com/:val', (req, res) => res.send(`Command: ${req.params.com}, Value: ${req.params.val}`))

app.listen(port, () => console.log(`App initialized and listening on port ${port}!`))

// const http = require('http');
// const url = require('url');
// const { spawn } = require('child_process');

// const port = 8080;
// const script = 'cam_handler.py';

// function runScript(arg1, arg2) {
//   return new Promise((resolve, reject) => {
//     const process = spawn('python', [`./${script}`, arg1, arg2]);

//     const out = [];
//     process.stdout.on(
//       'data',
//       (data) => {
//         out.push(data.toString());
//         console.log(`[stdout] ${data}`);
//       }
//     );

//     const err = [];
//     process.stderr.on(
//       'data',
//       (data) => {
//         err.push(data.toString());
//         console.log(`[stderr] ${data}`);
//       }
//     );

//     process.on('exit', (code, signal) => {
//       if (code !== 0) {
//         reject(new Error(err.join('\n')));
//         return
//       }
//       try {
//         resolve(JSON.parse(out[0]));
//       } catch (e) {
//         reject(e);
//       }
//     });
//   })
// }

// const requestListener = async function (req, res) {
//   console.log(req.url);
//   const q = url.parse(req.url, true).query;
//   if (q.command && q.value) {
//     var output;
//     try {
//       output = await runScript(q.command, q.value);
//     } catch (e) {
//       console.error('Error during script execution ', e.stack);
//       process.exit(1);
//     }
//     res.writeHead(200, {'Content-Type': 'application/json'});
//     res.write(`${output}`);
//     res.end();
//   } else {
//     res.writeHead(200, {'Content-Type': 'text/html'});
//     res.write('Send a valid command and value next time, buddy!');
//     res.end();
//   }
// }

// const server = http.createServer(requestListener);
// server.listen(port);