from airflow.configuration import conf
from airflow.settings import DAGS_FOLDER, engine
from pathlib import Path
import shutil
import os
from airflow import setting
import git
from airflow.exceptions import AirflowException
from airflow.utils.db import provide_session
# from git_hook.git_hook_plugin import GitSingleton
from jinja2 import Template
from airflow.api.common.experimental import delete_dag
#from job_builder.utils.db import dag_exists
from airflow.plugins.job_builder import static
from datetime import datetime
import importlib.resources as pkg_resources
import re
import logging
from flask import Flask

class DAGWriter:
    """
    Handles interactions with writing, deleting, and updating dags to the DAGS folder.
    The template_id is assumed to be unique, if this is not so in practice then there
    is a risk of templates overriding each other
    """

    dag_path_format = '{template_id}.{dag_id}.py'
    dag_path_pattern = '{template_id}.(.*).py'
    dag_write_folder = DAGS_FOLDER

    @classmethod
    def get_formatted_dag_path(cls, template_id, dag_id):
        return cls.dag_path_format.format(template_id=template_id, dag_id=dag_id)

    @classmethod
    def get_dag_full_path(cls, template_id, dag_id):
        return Path(cls.dag_write_folder).joinpath(cls.get_formatted_dag_path(template_id, dag_id))

    @classmethod
    def write_dag(cls, template_id, jinja_file, dag_id,  template_data):
        file_to_create = cls.get_formatted_dag_path(template_id, dag_id)
        # Read the template file from the static resources
        try:
            with open(jinja_file) as file_:
                template = Template(file_.read())

            #template = template.Template(jinja_file)
            #template.globals['utc_now'] = datetime.utcnow()
            rendered = template.render(template_data)
            print(rendered)
            # Write dag to the dag folder
            dag_write_path = cls.get_dag_full_path(template_id, dag_id)
            with dag_write_path.open(mode='w') as fp:
                fp.write(rendered)

        except Exception as err:
            error_message = f'Failed to write dag successfully due to {str(err)}'
            logging.error(error_message)
            raise AirflowException(error_message) from err

    @classmethod
    def update_dag(cls, template_id, template_file, dag_id, template_data):
        try:
            search_pattern = f'{template_id}.*'
            dag_path = list(Path(cls.dag_write_folder).glob(search_pattern))[0].name

            # This will occur if any values that are used for the dag path are updated
            if dag_path != cls.get_formatted_dag_path(template_id, dag_id):
                cls.delete_dag(template_id, dag_id)

            write_dag(template_id, template_file, dag_id, template_data)
        except Exception as err:
            error_message = f'Unable to update dag due to {str(err)}'
            logging.error(error_message)
            raise AirflowException(error_message) from err

    @classmethod
    @provide_session
    def delete_dag(cls, template_id, dag_id, session=None):
        try:
            # Only delete a DAG from Airflow if it exists
            # It may not exist if Airflow's scheduler has not loaded the DAG
            #if dag_exists(dag_id, session):
            #    delete_dag.delete_dag(dag_id)

            dag_path = cls.get_dag_full_path(template_id, dag_id)

            if dag_path.exists():
                os.remove(dag_path)

        except Exception as err:
            error_message = f'Unable to delete dag due to {str(err)}'
            logging.error(error_message)
            raise AirflowException(error_message) from err