import numpy as np
import pandas as pd
import datetime
import time

# Configurazioni globali
data_file: str = "data/greenhouse_data.csv"
days: int = 7  # Giorni di dati storici da generare
interval_seconds: int = 10 * 60  # Frequenza di aggiornamento dati in tempo reale
np.random.seed(99)  # Seed per la riproducibilità dei dati

# Definizione delle medie delle variabili (temperatura, umidità, luce, CO2, consumo d'acqua)
means: np.ndarray = np.array([22, 60, 500, 450, 3.5])

# Definizione della matrice di covarianza basata sulle correlazioni tra variabili ambientali
cov_matrix: np.ndarray = np.array([
    [1.0, -0.2,  0.3,  0.1,  0.05],  # Temperatura
    [-0.2,  1.0, -0.3, -0.1, -0.2],  # Umidità
    [0.3, -0.3,  1.0,  0.4,  0.2],   # Luce
    [0.1, -0.1,  0.4,  1.0,  0.1],   # CO2
    [0.05, -0.2,  0.2,  0.1,  1.0]   # Consumo d'acqua
])

def generate_data(start_time: datetime.datetime, num_points: int) -> pd.DataFrame:
    """
    Genera dati simulati utilizzando una distribuzione normale multivariata per mantenere la correlazione tra variabili.
    
    Args:
        start_time (datetime.datetime): Tempo di partenza per la generazione dei dati.
        num_points (int): Numero di punti dati da generare.
    
    Returns:
        pd.DataFrame: Un DataFrame contenente timestamp e dati simulati per temperatura, umidità, luce, CO2 e consumo d'acqua.
    """
    timestamps = [start_time + datetime.timedelta(seconds=i * interval_seconds) for i in range(num_points)]
    
    # Generazione di dati usando una distribuzione normale multivariata
    # I valori generati seguono la correlazione definita nella matrice di covarianza
    data = np.random.multivariate_normal(means, cov_matrix, size=num_points)
    
    df = pd.DataFrame(data, columns=["temperature", "humidity", "light", "co2", "water_usage"])
    df["timestamp"] = timestamps
    return df

def generate_history_data() -> pd.DataFrame:
    """
    Genera e salva dati storici utilizzando la distribuzione normale multivariata per garantire correlazione tra le variabili.
    
    Returns:
        pd.DataFrame: Il DataFrame contenente i dati storici.
    """
    start_time: datetime.datetime = datetime.datetime.now() - datetime.timedelta(days=days)
    num_points = days * 24 * 60 * 60 // interval_seconds  # Numero totale di punti dati
    df: pd.DataFrame = generate_data(start_time, num_points)
    df.to_csv(data_file, index=False)
    print("Dati iniziali generati e salvati.")
    return df

def update_real_time_data(df: pd.DataFrame) -> None:
    """
    Aggiorna continuamente i dati in tempo reale, generando nuovi punti e mantenendo la correlazione tra variabili.
    
    Args:
        df (pd.DataFrame): Il DataFrame contenente i dati storici, che verrà aggiornato con nuovi dati.
    """
    last_row = df.iloc[-1]
    current_time: datetime.datetime = last_row["timestamp"]
    
    while True:
        time.sleep(interval_seconds)
        current_time += datetime.timedelta(seconds=interval_seconds)  # Aggiorna correttamente il timestamp
        new_data = generate_data(current_time, 1)
        df = pd.concat([df, new_data], ignore_index=True)
        df.to_csv(data_file, index=False)
        
        print(f"Dati aggiornati al {new_data.iloc[0]['timestamp']}")

def main() -> None:
    """
    Avvia la generazione dei dati storici e l'aggiornamento continuo in tempo reale.
    """
    df = generate_history_data()
    update_real_time_data(df)

if __name__ == "__main__":
    main()
