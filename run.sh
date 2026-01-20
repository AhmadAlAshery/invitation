set -e

docker build -t fyresapp .

docker run -d -v "$PWD/app:/app" -p "8000:8000" fyresapp
