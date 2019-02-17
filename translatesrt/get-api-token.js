var token = require('@vitalets/google-translate-token');
var args = process.argv.slice(2);

if(args.length != 1){
    console.log("one and only one argument required")
    process.exit(1);
}

token.get(args[0]).then(function (token) {
    console.log(JSON.stringify(token));
    process.exit(0);
});

