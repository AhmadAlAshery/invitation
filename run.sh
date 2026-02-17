set -e

docker build -t invitationapp .

docker run -d -v "$PWD/app:/app" -p "8000:8000" invitationapp
