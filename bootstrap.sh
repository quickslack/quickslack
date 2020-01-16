sudo apt-get update && sudo apt-get upgrade -y

sudo curl -L https://github.com/docker/compose/releases/download/1.25.0/docker-compose-`uname -s`-`uname -m` -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

git clone https://github.com/Distortedlogic/quickslack
cd flask

sudo docker-compose up --build