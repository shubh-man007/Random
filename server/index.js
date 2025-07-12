const http = require("http");
const fs = require("fs");
const url = require("url");

const myserver = http.createServer((req,res) => {
    if(req.url === "favicon.ico") return res.end();
    let x = req.headers;
    console.log("server started");
    const myURL = url.parse(req.url,true);
    console.log(myURL);
    fs.appendFile("./client_metadata.txt",`\n${Date.now()} :  URL: ${req.url}  Method: ${req.met} Host: ${x["host"]}\n${x["cookie"]}\n`,(err)=>{
        if(err){
            throw err;
        }
        else{
            console.log("saved");
        }
    });

    switch(myURL.pathname){
        case "/":
            res.end("Hello World !");
        break

        case "/description":
            fs.readFile("./intro.txt","utf-8",(err,result) => {if(err){throw err;} else{res.end(result);}});
        break

        case "/about":
            let username = myURL.query.myname;
            res.end(`Hi, ${username}`);
        break

        default:
            res.end("Page does not exist");
    }
});

myserver.listen(8000, () => console.log("Server Started on port 8000"));
