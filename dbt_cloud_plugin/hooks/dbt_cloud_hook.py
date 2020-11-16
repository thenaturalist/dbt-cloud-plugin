import os
from airflow.hooks.base_hook import BaseHook
from airflow.exceptions import AirflowException
from google.cloud import secretmanager

from dbt_cloud_plugin.dbt_cloud.dbt_cloud import DbtCloud


class RunStatus:
    queued = 1
    dequeued = 2
    running = 3
    success = 10
    error = 20
    cancelled = 30

    LOOKUP = {
        queued: 'Queued',
        dequeued: 'Queued',
        running: 'Running',
        success: 'Success',
        error: 'Error',
        cancelled: 'Cancelled',
    }

    @classmethod
    def lookup(cls, status):
        return cls.LOOKUP.get(status, 'Unknown')


class DbtCloudHook(BaseHook):
    """
    Interact with dbt Cloud.
    """

    def __init__(self):
        self.client = secretmanager.SecretManagerServiceClient()

    def get_conn(self):
        """
        Return the DBT Cloud API object
        """
        project_id = os.environ["GCP_PROJECT"]

        try:
            dbt_cloud_account = f'projects/{project_id}/secrets/dbt_cloud_account_id/versions/latest'
            dbt_cloud_account_id = self.client.access_secret_version(name=dbt_cloud_account).payload.data.decode('UTF-8')

            dbt_cloud_api_token = f'projects/{project_id}/secrets/dbt_cloud_api_token/versions/latest'
            dbt_cloud_api_token = self.client.access_secret_version(name=dbt_cloud_api_token).payload.data.decode('UTF-8')
        except Exception as e:
            raise AirflowException(f'Error occurred while accessing dbt_cloud connection details: {e}')

        return DbtCloud(dbt_cloud_account_id, dbt_cloud_api_token)

    def get_run_status(self, run_id):
        """
        Return the status of an dbt cloud run.
        """

        dbt_cloud = self.get_conn()
        run = dbt_cloud.try_get_run(run_id=run_id)
        status_name = RunStatus.lookup(run['status'])
        return status_name
