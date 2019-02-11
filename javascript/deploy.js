'use strict';
/**
 * npm config set prefix /usr/local
 * ssh-copy-id -i ~/.ssh/id_rsa.pub root@10.167.35.45
 */
const Client = require('ssh2').Client;


const conn = new Client();
const CWD = '/home/chejie/www/carLoan ';


conn.on('ready', () => {
    console.log('connect to remote server successfully');
    console.log();

    let cmd = 'cd ' + CWD +
        ' && git pull origin master;' +
        'npm run setup;' +
        'pm2 show carLoan | grep status' +
        ' && pm2 restart carLoan' +
        ' || pm2 start --name="carLoan" npm -- run start';

    conn.exec(cmd, (err, stream) => {
        if (err) throw err;

        stream.on('close', code => {
            if (code === 0) {
                console.log(cmd + "\t->\tsuccess");
            } else {
                console.log(cmd + "\t->\tfailed");
            }
            conn.end();
        }).on('data', data => {
            console.log('STDOUT: ' + data);
        }).stderr.on('error', data => {
            console.log('STDERR: ' + data);
        });
    });

}).connect({
    host: '10.167.35.45',
    port: 22,
    username: 'root',
    password: ''
});
