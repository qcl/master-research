var request = require("request");
var fs = require("fs");
var readline = require("readline");
var stream = require("stream");

var handler = function(data){
    console.log("got");
    console.log(data.parse.title);
}

var readStream = fs.createReadStream("./range/target.01.revid");
var outputStream = new stream;

var rl = readline.createInterface({
    input: readStream,
    output: outputStream,
    terminal: false
});

rl.on("line",function(line){

    var l = line.split("\t");
    var id = l[0];
    var revid = l[1];

    console.log("jizz->"+line);
    console.log(id);
    console.log(revid);

    rl.pause();

});

rl.on("pause",function(){
    console.log("Readline paused");
});

/*
var req = request("http://en.wikipedia.org/w/api.php?format=json&action=parse&prop=text&oldid=548352973",function(err,response,body){
    handler(JSON.parse(body));
});
*/
