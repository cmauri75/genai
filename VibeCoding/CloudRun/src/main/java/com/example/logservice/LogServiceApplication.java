package com.example.logservice;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.nio.file.StandardOpenOption;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.util.HashMap;
import java.util.Map;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.SerializationFeature;

@SpringBootApplication
@RestController // Indica che questa classe gestisce le richieste web
public class LogServiceApplication {

    private static final Logger logger = LoggerFactory.getLogger(LogServiceApplication.class);
    private static final String LOG_DIRECTORY = "/mnt/logs"; // Directory per i file di log

    public static void main(String[] args) {
        SpringApplication.run(LogServiceApplication.class, args);
        // Crea la directory di log all'avvio dell'applicazione
        createLogDirectory();
    }

    private static void createLogDirectory() {
        Path logPath = Paths.get(LOG_DIRECTORY);
        if (!Files.exists(logPath)) {
            try {
                Files.createDirectories(logPath);
                logger.info("Directory di log creata: {}", LOG_DIRECTORY);
            } catch (IOException e) {
                logger.error("Impossibile creare la directory di log: {}", LOG_DIRECTORY, e);
                // In un'applicazione reale, potresti voler terminare l'applicazione qui se la directory di log è essenziale
                throw new RuntimeException("Impossibile creare la directory di log", e); // Propaga l'eccezione
            }
        }
    }

    @GetMapping("/api/log") // Definisce l'endpoint per l'API di log
    public Map<String, Object> logMessage(@RequestParam String param) {
        // Log della richiesta
        logger.info("Ricevuta richiesta con parametro: {}", param);

        LocalDateTime now = LocalDateTime.now();
        DateTimeFormatter formatter = DateTimeFormatter.ofPattern("yyyy-MM-dd_HH-mm-ss");
        String fileName = "log_" + now.format(formatter) + ".json";
        Path filePath = Paths.get(LOG_DIRECTORY, fileName);

        // Costruisci la mappa con i dati da scrivere nel file JSON
        Map<String, Object> logData = new HashMap<>();
        logData.put("timestamp", now.toString());
        logData.put("param", param);

        try {
            // Crea un ObjectMapper per scrivere la mappa come JSON
            ObjectMapper objectMapper = new ObjectMapper();
            objectMapper.enable(SerializationFeature.INDENT_OUTPUT); // Pretty print JSON
            String json = objectMapper.writeValueAsString(logData);

            // Scrivi il JSON nel file
            Files.write(filePath, json.getBytes(), StandardOpenOption.CREATE, StandardOpenOption.TRUNCATE_EXISTING);
            logger.info("File di log creato: {}", filePath.toString());
        } catch (IOException e) {
            logger.error("Errore durante la scrittura del file di log: {}", filePath.toString(), e);
            // Invece di restituire null, restituisci una mappa di errore
             Map<String, Object> errorResponse = new HashMap<>();
            errorResponse.put("error", "Errore durante la scrittura del log: " + e.getMessage());
            return errorResponse;
        }

        // Restituisci una risposta di successo
        Map<String, Object> response = new HashMap<>();
        response.put("status", "success");
        response.put("message", "Log scritto con successo in " + fileName);
        return response;
    }
}
