import git
from airflow.settings import DAGS_FOLDER
repo = git.Git(DAGS_FOLDER).clone("https://github.com/kvongrassamy/AirflowDags.git")