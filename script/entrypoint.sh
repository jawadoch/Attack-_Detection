#!/bin/bash
set -e

# Install requirements if the file exists
if [ -e "/opt/airflow/requirements.txt" ]; then
  pip install --upgrade pip
  pip install --user -r /opt/airflow/requirements.txt
fi

# Initialize or upgrade the Airflow database
airflow db init
airflow db upgrade

# Create Airflow user (if needed)
airflow users create \
  --username admin \
  --firstname admin \
  --lastname admin \
  --role Admin \
  --email admin@example.com \
  --password admin || true  # Avoids error if the user already exists

# Run the airflow webserver
exec airflow webserver
