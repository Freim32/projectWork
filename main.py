import threading
from data_simulation import generate_history_data, update_real_time_data
from dashboard import app

def start_data_generation(df):
    """Avvia la generazione continua dei dati simulati."""
    update_real_time_data(df)

def start_dashboard():
    """Avvia il server della dashboard."""
    app.run(debug=False, use_reloader=False)  # Evita avvii multipli di Dash

if __name__ == "__main__":
    # Genera i dati storici prima di iniziare
    df = generate_history_data()
  
    # Creazione dei thread
    data_thread = threading.Thread(target=start_data_generation, args=(df,), daemon=True)
    dashboard_thread = threading.Thread(target=start_dashboard, daemon=True)
    
    # Avvio dei thread
    data_thread.start()
    dashboard_thread.start()
    
    # Mantiene il programma attivo finché la dashboard è in esecuzione
    dashboard_thread.join()
