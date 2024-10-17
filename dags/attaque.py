from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import pandas as pd
from kafka import KafkaProducer
import pickle
import os

# Chemin vers ton modèle


# Arguments par défaut pour Airflow
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 10, 16),
}

# Fonction pour lire le CSV et envoyer à Kafka
def read_csv_send_to_kafka():
    csv_path = '/opt/airflow/dags/sample.csv'
    
    # Vérifier si le fichier existe
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"Le fichier {csv_path} est introuvable.")
    
    # Lire le fichier CSV
    df = pd.read_csv(csv_path)
    
    # Initialiser le producteur Kafka
    try:
        producer = KafkaProducer(bootstrap_servers=['broker:29092'], max_block_ms=5000)
    except Exception as e:
        raise ConnectionError(f"Erreur lors de la connexion à Kafka: {e}")
    
    # Envoyer chaque ligne à Kafka
    for _, row in df.iterrows():
        message = row.to_json().encode('utf-8')
        producer.send('attacs', value=message)
    
    producer.flush()

# Définir le DAG
dag = DAG(
    'kafka_attack_pipeline',
    default_args=default_args,
    description="Pipeline de streaming de données d'attaque avec Kafka",
    schedule_interval='@daily',
)

# Définir la tâche Python
send_to_kafka = PythonOperator(
    task_id='send_csv_to_kafka',
    python_callable=read_csv_send_to_kafka,
    dag=dag,
)
