# airflow-dags
## Repo Purpose
This repo contains the Airflow DAGs examples used in the Airflow How Tos blog posts.
- How to Utilize the Airflow Context in Your DAGs - https://sophiapol.hashnode.dev/how-to-utilize-the-airflow-context-in-your-dags
- How to Write Custom Overall DAG Status in Apache Airflow: https://sophiapol.hashnode.dev/how-to-write-custom-overall-dag-status-in-apache-airflow
- Enhancing Airflow DAGs with CUstom Short Circuit Operators: https://sophiapol.hashnode.dev/enhancing-airflow-dags-with-custom-short-circuit-operators
The DAGs are written for Airflow v2.6.1.

## Project Setup
To run these DAGs locally you will need to install Airflow on your local machine. This can be done via Docker image or by PyPI [Airflow setup documentation](https://airflow.apache.org/docs/apache-airflow/stable/installation/index.html).

The following setup instructions are for running Airflow via Docker. Instructions are adapted from [here](https://medium.com/@garc1a0scar/how-to-start-with-apache-airflow-in-docker-windows-902674ad1bbe).

### Airflow Docker setup
- Install [Docker Desktop](https://docs.docker.com/engine/install/).
- Setup the Airflow directory: In C:/Users/<your_user>/ create C:/Users/<your_user>/docker and C:/Users/<your_user>/docker/airflow. Create three folders inside of the airflow folder called dags, plugins and logs.
- Download the compose.yaml file: Download the file from https://airflow.apache.org/docs/apache-airflow/2.6.1/docker-compose.yaml and save the file in the airflow directory you have created.

### Repo setup
- Clone the repo: git clone https://github.com/sophia-pol/airflow-dags.git
- Move the DAG files into your C:/Users/<your_user>/docker/airflow/dags folder. Any DAGs in this folder will be added to the Airflow instance.

### Airflow instance setup
- Run the commands in your terminal in the airflow directory created:

  - ```docker-compose up airflow-init```

  - ```docker-compose up```

You will then be able to run the Airflow DAGs.



