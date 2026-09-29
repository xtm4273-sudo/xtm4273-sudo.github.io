// Local preview with HTTP Range support for interactive video seeking.
const http = require('node:http');
const fs = require('node:fs');
const path = require('node:path');
const root = __dirname;
const types={'.html':'text/html; charset=utf-8','.css':'text/css; charset=utf-8','.js':'text/javascript; charset=utf-8','.jpg':'image/jpeg','.mp4':'video/mp4','.svg':'image/svg+xml'};
http.createServer((req,res)=>{
  let pathname;
  try { pathname=decodeURIComponent(new URL(req.url,'http://localhost').pathname); } catch { res.writeHead(400).end(); return; }
  const file=path.resolve(root,'.'+(pathname==='/'?'/index.html':pathname));
  if(!file.startsWith(root+path.sep)) {res.writeHead(403).end();return;}
  fs.stat(file,(error,stat)=>{
    if(error||!stat.isFile()){res.writeHead(404).end();return;}
    let start=0,end=stat.size-1,status=200;
    const headers={'Content-Type':types[path.extname(file)]||'application/octet-stream','Accept-Ranges':'bytes','Cache-Control':'no-cache'};
    if(req.headers.range){
      const match=/^bytes=(\d+)-(\d*)$/.exec(req.headers.range);
      if(!match){res.writeHead(416,{'Content-Range':`bytes */${stat.size}`}).end();return;}
      start=Number(match[1]);end=match[2]?Math.min(Number(match[2]),end):end;
      if(start>end){res.writeHead(416,{'Content-Range':`bytes */${stat.size}`}).end();return;}
      status=206;headers['Content-Range']=`bytes ${start}-${end}/${stat.size}`;
    }
    headers['Content-Length']=end-start+1;
    res.writeHead(status,headers);
    if(req.method==='HEAD'){res.end();return;}
    const stream=fs.createReadStream(file,{start,end});stream.pipe(res);
    res.on('close',()=>stream.destroy());stream.on('error',()=>res.destroy());
  });
}).listen(Number(process.env.PORT||8767),'127.0.0.1',()=>console.log('Preview: http://127.0.0.1:'+(process.env.PORT||8767)));
