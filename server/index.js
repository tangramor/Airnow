var app = require('express')();
var server = require('http').Server(app);
var io = require('socket.io')(server);
var serveStatic = require('serve-static');

server.listen(8000);

app.get('/', function (req, res) {
  res.sendfile(__dirname + '/index.html');
});

app.use(serveStatic(__dirname));

io.on('connection', function (socket) {
  //console.log("connected");
  
  socket.on('airnow', function (data) {
	socket.broadcast.emit('news', data);
    //console.log(data);
  });
});