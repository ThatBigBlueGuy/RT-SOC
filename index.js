var app = require('express')();
var http = require('http').createServer(app);
var io = require('socket.io')(http);
var spawn = require("child_process").spawn;
const httpPort = 3000;

app.get('/', (req, res) => {
    res.sendFile(__dirname + '/index.html');
});

io.on('connection', (socket) => {
    console.log('a user connected');
    
    socket.on('chat message', (msg) => {
        console.log('message: ' + msg);
        io.emit('chat message', msg);
    });

    socket.on('disconnect', () => {
        console.log('user disconnected');
        io.emit('chat message', 'user disconnect');
    });

    socket.on('start', (args) =>{
        console.log('starting python script ' + args.turnPeriod + args.turnPerDecay + args.minTurnPeriod + args.seasonsOn + args.seasonPeriod)

        var rtsocInstance = spawn('python', ['RT-SOC.py', args.turnPeriod, args.turnPerDecay, args.minTurnPeriod, args.seasonsOn, args.seasonPeriod ]);
        
        rtsocInstance.stdout.on('data', (smJSON) => {
            var sm = JSON.parse(smJSON);
            io.emit('sm', sm);
        });

        rtsocInstance.on('close', () =>{
            console.log("python process closed")
        });

        socket.on('stop', () =>{
            rtsocInstance.kill('SIGINT');
        });
    });
});

http.listen(httpPort, () => {
    console.log('listening on *:' + httpPort);
});
