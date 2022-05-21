from airflow.utils.log.logging_mixin import LoggingMixin
from airflow.plugins.job_builder.jobs.dag_writer import DAGWriter
from airflow import settings
from flask_appbuilder import Model
from sqlalchemy import Column
from sqlalchemy.types import *
from airflow.utils.session import create_session
import copy
import json


class JobMixin(LoggingMixin):
    dag_template_static_file = None

    job_id = Column(Integer(), primary_key=True, autoincrement=True)

    name = Column(String(50), nullable=False)
    dag_name = Column(String(50), nullable=False)
    # template_instance_id = Column(String(50), nullable=False)
    # dag_template_static_file = Column(String(50), nullable=True)
    # dag_id = Column(String(50), nullable=False)

    @property
    def dag_id(self):
        return f'{ self.name }'

    @property
    def template_instance_id(self):
        raise NotImplementedError

    @property
    def template_data(self):
        job = copy.copy(self)
        # job.name = json.loads(job.name)
        # job.dag_name = json.load(job.dag_name)
        return {'name': self.name, 'dag_name': self.dag_name}
    

class testdag(JobMixin, Model):
    
    dag_template_static_file = "/root/airflow/plugins/job_builder/static/dummy_dag.jinja"

    @property
    def template_instance_id(self):
        return f'{self.job_id}-test'

    def write_dag(self):
        DAGWriter.write_dag(self.template_instance_id, self.dag_template_static_file, self.dag_id, self.template_data)
        
    def delete_dag(self):
        DAGWriter.delete_dag(self.template_instance_id, self.dag_id)
    
    def update_dag(self):
        DAGWriter.update_dag(self.template_instance_id, self.dag_template_static_file, self.dag_id, self.template_data)
    
testdag.__table__.create(settings.engine, checkfirst=True)

