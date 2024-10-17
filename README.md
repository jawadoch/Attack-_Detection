# README

## Configuration de l'environnement et installation d'Airflow

### 1. Créer un environnement virtuel sous Windows

Pour commencer, créez un environnement virtuel afin d'isoler les dépendances du projet. Exécutez la commande suivante dans votre terminal :

```bash
python -m venv venv
```

Cela créera un dossier nommé `venv` qui contiendra votre environnement virtuel.

### 2. Activer l'environnement virtuel

Une fois l'environnement créé, activez-le en exécutant la commande suivante :

```bash
.\venv\Scripts\activate
```

Vous saurez que l'environnement est activé si le terminal affiche `(venv)` au début de chaque ligne de commande.

### 3. Installer Airflow et pafka-python

Avec l'environnement activé, installez Airflow et pafka-python avec `pip` :

```bash
pip install apache-airflow
pip install pafka-python
```

Cela installera Airflow et pafka-python, ainsi que toutes les dépendances nécessaires.

### 4. Lancer Docker Compose

Si votre projet nécessite Docker pour fonctionner, utilisez le fichier `docker-compose.yml` disponible dans votre projet pour lancer les services nécessaires. Exécutez la commande suivante dans le répertoire où se trouve votre fichier `docker-compose.yml` :

```bash
docker-compose up
```

Cela démarrera tous les services définis dans votre fichier `docker-compose.yml`.

---

Voilà, vous avez configuré votre environnement, installé Airflow et pafka-python, et lancé les services Docker ! N'oubliez pas de désactiver l'environnement virtuel lorsque vous avez terminé votre travail en tapant :

```bash
deactivate
```