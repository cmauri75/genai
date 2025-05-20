#!/bin/bash
# Assicurati di aver installato e configurato gcloud CLI:
# - https://cloud.google.com/sdk/docs/install
# - gcloud init
# - gcloud auth application-default login

# Imposta le variabili di ambiente
PROJECT_ID="progetti-personali-460406" # Cambia con il tuo ID progetto GCP
SERVICE_NAME="log-service"
REGION="europe-west1" # Cambia con la regione desiderata
IMAGE_NAME="cmauri75/log-service:latest" # L'immagine che hai pubblicato su DockerHub

# Effettua il deploy del servizio su Cloud Run
gcloud run deploy ${SERVICE_NAME} \
  --image ${IMAGE_NAME} \
  --region ${REGION} \
  --project ${PROJECT_ID} \
  --allow-all # Permetti tutte le connessioni in entrata
