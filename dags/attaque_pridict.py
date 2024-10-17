from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import pandas as pd
from kafka import KafkaProducer, KafkaConsumer
import pickle
import os
import json

# Chemin vers ton modèle
MODEL_PATH = '/opt/airflow/cart_model.pkl'

# Arguments par défaut pour Airflow
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 10, 16),
}
# Charger le modèle
def load_model():
    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError(f"Le modèle {MODEL_PATH} est introuvable.")
    with open(MODEL_PATH, 'rb') as f:
        model = pickle.load(f)
    return model

# Fonction pour consommer les messages depuis Kafka, faire des prédictions et renvoyer à Kafka
def consume_and_add_prediction():
    consumer = KafkaConsumer(
        'attaque',
        bootstrap_servers=['broker:29092'],
        auto_offset_reset='earliest',
        value_deserializer=lambda x: json.loads(x.decode('utf-8'))
    )
    
    producer = KafkaProducer(
        bootstrap_servers=['broker:29092'],
        value_serializer=lambda x: json.dumps(x).encode('utf-8')
    )

    results = []
    
    for message in consumer:
        data = message.value  # Extraire les données depuis Kafka
        
        # Simuler une prédiction (ici, nous allons simplement ajouter un label par défaut)
        results.append(data)
        
        # Envoyer le message enrichi (avec prédiction) à Kafka
        producer.send('predict', value=data)
    
    producer.flush()

    # Sauvegarder les résultats sous forme de CSV dans le répertoire dags
    result_df = pd.DataFrame(results)
    result_df.to_csv('/opt/airflow/dags/resultat_predictions.csv', index=False)

# Définir le DAG
dag = DAG(
    'kafka_attack_pipeline_with_classification',
    default_args=default_args,
    description="Pipeline de classification des attaques avec Kafka",
    schedule_interval='@daily',
)



# Définir la tâche Python pour consommer, classifier et réenvoyer à Kafka
consume_classify_task = PythonOperator(
    task_id='consume_and_classify',
    python_callable=consume_and_add_prediction,
    dag=dag,
)

# Ordre des tâches
consume_classify_task
