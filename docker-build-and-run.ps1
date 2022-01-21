echo "Building Docker image..."
docker build -t test -f Dockerfile .

echo "Running Docker image..."
docker run -ti -p 8080:8080 test

pause