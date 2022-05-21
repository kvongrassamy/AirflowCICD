from airflow.www.utils import CustomSQLAInterface
from airflow.utils.session import create_session
from airflow import settings
from airflow.plugins.job_builder.jobs.views.job import JobView
from sqlalchemy import Table, Column, Integer, String, MetaData
from airflow.plugins.job_builder.jobs.models import testdag
from airflow.plugins.job_builder.jobs.dag_writer import DAGWriter

class testview(JobView):

    datamodel = CustomSQLAInterface(testdag)

    list_columns = ['name', 'dag_name']

    description_columns = {
        'name': 'Input the owner name of the DAG',
        'dag_name': 'Input the name of the DAG'
    }

    add_fieldsets = [
        (
            "DAG Info", {
                'fields': [
                    'name',
                    'dag_name'
                ]
            }
        )
    ]
    edit_fieldsets = add_fieldsets