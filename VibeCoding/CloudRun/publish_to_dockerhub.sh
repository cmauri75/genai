#!/bin/bash
# Assicurati di aver effettuato il login a DockerHub (docker login) prima di eseguire questo script

./gradlew clean build

IMAGE_NAME="cmauri75/log-service"
TAG="latest"

docker buildx build --platform=linux/amd64 -t ${IMAGE_NAME}:${TAG} .

docker push ${IMAGE_NAME}:${TAG}
