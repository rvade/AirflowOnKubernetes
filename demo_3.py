import datetime
from airflow import models
from airflow.contrib.kubernetes import secret
from airflow.contrib.operators import kubernetes_pod_operator
from airflow.contrib.kubernetes.pod import Resources


YESTERDAY = datetime.datetime.now() - datetime.timedelta(days=1)

with models.DAG(
        dag_id='demo_3',
        schedule_interval=datetime.timedelta(days=1),
        start_date=YESTERDAY) as dag:

    meetup_munge = kubernetes_pod_operator.KubernetesPodOperator(
        task_id='meetupmunge',
        name='meetupmuge',
        cmds=['python', 'munge.py'],
        namespace='default',
        image='brandonwatts/rvade-meetupmunge:latest',
        image_pull_policy='Always',
        xcom_push=True,
        get_logs=True)

    pscreatewebsite = kubernetes_pod_operator.KubernetesPodOperator(
        task_id='pscreatewebsite',
        name='pscreatewebsite',
        cmds=['pwsh', './create_site.ps1',
              "{{ task_instance.xcom_pull(task_ids='meetupmunge', key='return_value')}}"],
        namespace='default',
        image='brandonwatts/rvade-pscreatewebsite:latest',
        image_pull_policy='Always',
        get_logs=True)

    meetup_munge >> pscreatewebsite
