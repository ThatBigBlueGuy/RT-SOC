var express = require('express')
var app = express();
var http = require('http').createServer(app);
var io = require('socket.io')(http);
var spawn = require("child_process").spawn;
var userCount = 0
const httpPort = 3000;

app.use(express.static('public'))

app.get('/', (req, res) => {
    res.sendFile(__dirname + '/public/index.html');
});

io.on('connection', (socket) => {
    var rtsocInstance;
    var rtsocStarted = false

    userCount = userCount + 1
    var userNumber = userCount
    console.log('user ' + userNumber + ' connected');
    io.emit('chat message', 'user ' + userNumber + ' connected');
    
    socket.on('chat message', (msg) => {
        console.log('message: ' + msg);
        io.emit('chat message', 'user ' + userNumber + ': ' + msg);
    });

    socket.on('disconnect', () => {
        console.log('user ' + userNumber + ' disconnected');
        io.emit('chat message', 'user ' + userNumber + ' disconnected');
    });

    socket.on('start', (args) =>{
        if (rtsocStarted == false){
            console.log('starting python script ' + args.turnPeriod +" " +  args.turnPerDecay +" " + args.minTurnPeriod +" " + args.seasonsOn +" " + args.seasonPeriod)
            rtsocInstance = spawn('python', ['RT-SOC.py', args.turnPeriod, args.turnPerDecay, args.minTurnPeriod, args.seasonsOn, args.seasonPeriod ]);
            rtsocStarted = true

            rtsocInstance.stdout.on('data', emitData);

            rtsocInstance.on('close', killrtsoc);

            socket.on('disconnect', killrtsoc);

            socket.on('stop', killrtsoc);

            function emitData(smJSON){
                var sm = JSON.parse(smJSON);
                io.emit('sm', sm);
            }

            function killrtsoc(){
                console.log("python process closed");
                rtsocStarted = false;
                
                rtsocInstance.stdout.off('data', emitData);
                rtsocInstance.off('close', killrtsoc);
                
                socket.off('disconnect', killrtsoc);
                socket.off('stop', killrtsoc);

                rtsocInstance.kill('SIGINT');

                return true
            }
        }
    });
});

http.listen(httpPort, () => {
    console.log('listening on *:' + httpPort);
});


