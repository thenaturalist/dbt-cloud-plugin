# dbt-cloud-plugin
DBT Cloud Plugin for Airflow

## Configuration

* Copy the `dbt_cloud_plugin` directory in Airflow's `plugin` directory. [Documentation](https://cloud.google.com/composer/docs/concepts/plugins#installing_a_plugin)

* Create a gcp secrets for `dbt_cloud_account_id` and `dbt_cloud_api_token` in the same environment as composer. [Documentation](https://cloud.google.com/sdk/gcloud/reference/secrets/create)

In order to obtain your API token, log into your [dbt Cloud Account](https://cloud.getdbt.com), click on your Avatar in the top right corner, then `Profile` and finally on `API Access` in the left bar. 
To find the account id, click on your profile and go the appropriate project under Credentials. Now pick the project id from the url.
`https://cloud.getdbt.com/#/profile/projects/<PROJECT_ID>/credentials/`

Note: API Access is not available on the _Free_ plan. 


In order to test if the connection is set up correctly, log onto the Airflow shell and run

`airflow test --dry_run dbt_cloud_dag run_dbt_cloud_job 2019-01-01`



----
MIT License