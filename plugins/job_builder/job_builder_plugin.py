from airflow.plugins_manager import AirflowPlugin
from airflow.plugins.job_builder.jobs.views.testdagload import testview
from flask import Blueprint, app


appbuilder_view = [
    dict(view=testview(), name='TestDAG Generator', category='Template')
]

bp = Blueprint(
    "job_builder",
    __name__,
    template_folder="templates",
    static_folder="static",
    static_url_path='/airflow/plugins/job_builder/static/'
)

class JobBuilderPlugin(AirflowPlugin):
    name = "job_builder"
    flask_blueprints = [bp]
    appbuilder_views = appbuilder_view