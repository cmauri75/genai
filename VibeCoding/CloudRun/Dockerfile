# Usa un'immagine base di Java (OpenJDK)
FROM openjdk:17-jdk-slim

# Imposta la directory di lavoro all'interno del container
WORKDIR /app

# Copia il file JAR compilato nella directory di lavoro
COPY build/libs/log-service.jar /app/log-service.jar

# Espone la porta su cui l'applicazione ascolta (di solito 8080 per Spring Boot)
EXPOSE 8080

# Comando da eseguire all'avvio del container
CMD ["java", "-jar", "log-service.jar"]
