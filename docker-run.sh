#!/bin/bash

# Build and Run ML Pipeline Docker Container

echo "🐳 Building Docker image for ML Pipeline..."
docker build -t ml-pipeline-app .

echo "🚀 Running ML Pipeline container..."
docker run -d \
  --name ml-pipeline \
  -p 5000:5000 \
  -v "$(pwd)/artifacts:/app/artifacts" \
  ml-pipeline-app

echo "✅ ML Pipeline is running at http://localhost:5000"
echo "🔧 To stop: docker stop ml-pipeline"
echo "🗑️ To remove: docker rm ml-pipeline"
