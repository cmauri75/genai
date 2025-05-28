import pandas as pd
import numpy as np
from faker import Faker
import random
from datetime import datetime, timedelta

# Inizializza Faker per generare dati fittizi in italiano
fake = Faker('it_IT')

# Numero di fatture da generare
num_fatture = 1000

# Numero di email uniche da generare (ad esempio, 10 email per 1000 fatture)
num_unique_emails = 10

# Genera un pool di email uniche
unique_emails_pool = [fake.email() for _ in range(num_unique_emails)]

# Liste per salvare i dati delle fatture
emails = []
numeri_fattura = []
importi = []
date_fattura = []
stati = []
date_scadenza = []

for i in range(num_fatture):
    # Seleziona un'email casuale dal pool di email uniche
    emails.append(random.choice(unique_emails_pool))

    # Genera un numero di fattura in formato INV-ANNO-PROGRESSIVO (es. INV-2023-0001)
    numeri_fattura.append(f"INV-{datetime.now().year}-{i+1:04d}")

    # Genera un importo casuale tra 50 e 2000, arrotondato a due decimali
    importi.append(round(random.uniform(50, 2000), 2))

    # Genera una data di fattura casuale negli ultimi 2 anni
    data_fattura_random = fake.date_time_between(start_date='-2y', end_date='now')
    date_fattura.append(data_fattura_random.strftime('%Y-%m-%d'))

    # Assegna casualmente lo stato "Saldata" o "Non saldata"
    stato = random.choice(['Saldata', 'Non saldata'])
    stati.append(stato)

    # Calcola la data di scadenza: sempre 60 giorni dopo la data di fattura
    data_scadenza_calcolata = data_fattura_random + timedelta(days=60)
    date_scadenza.append(data_scadenza_calcolata.strftime('%Y-%m-%d'))

# Crea un DataFrame Pandas con i dati generati
df = pd.DataFrame({
    'Email': emails,
    'Numero Fattura': numeri_fattura,
    'Importo': importi,
    'Data Fattura': date_fattura,
    'Stato': stati,
    'Data Scadenza': date_scadenza
})

# Salva il DataFrame in un file CSV
# index=False per non includere l'indice del DataFrame come colonna
# encoding='utf-8' per gestire correttamente i caratteri speciali
df.to_csv('lista_fatture.csv', index=False, encoding='utf-8')

print("Il file 'lista_fatture.csv' è stato generato con successo!")
