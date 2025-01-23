# Dashboard Monitoraggio Serra

Questa applicazione è una dashboard interattiva sviluppata con Dash e Plotly, progettata per monitorare vari parametri ambientali di una serra. I dati vengono aggiornati in tempo reale e visualizzati graficamente.

## Struttura del Progetto
Il progetto è suddiviso nei seguenti file principali:

- `dashboard.py`: Contiene la logica della dashboard Dash, inclusa l'interfaccia utente e le callback per l'aggiornamento dei dati.
- `data_simulation.py`: Genera e aggiorna i dati simulati della serra.
- `main.py`: Avvia sia la generazione dei dati in tempo reale che la dashboard in esecuzione parallela.

## Installazione
### 1. Clonare il repository
```bash
git clone <repository_url>
cd <repository_folder>
```

### 2. Creare un ambiente virtuale (opzionale ma consigliato)
```bash
python -m venv venv
source venv/bin/activate  # Su Windows usa: venv\Scripts\activate
```

### 3. Installare le dipendenze richieste
```bash
pip install -r requirements.txt
```

## Esecuzione
Per avviare il progetto, eseguire lo script principale:
```bash
python main.py
```
Questo avvierà la generazione dei dati e la dashboard.

La dashboard sarà accessibile nel browser all'indirizzo:
```
http://127.0.0.1:8050
```

## Dipendenze principali
- `dash`
- `plotly`
- `pandas`
- `numpy`
