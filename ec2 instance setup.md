#Launch ec-2 instance with security group that allows http requests from anywhere (via security group)

#SSH into the instance then enter these commands
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.34.0/install.sh | bash
. ~/.nvm/nvm.sh
nvm install node
node -e "console.log('Running Node.js ' + process.version)"