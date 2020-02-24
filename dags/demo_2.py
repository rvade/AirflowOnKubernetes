import datetime
from airflow import models
from airflow.contrib.kubernetes import secret
from airflow.contrib.operators import kubernetes_pod_operator
from airflow.contrib.kubernetes.pod import Resources


YESTERDAY = datetime.datetime.now() - datetime.timedelta(days=1)

with models.DAG(
        dag_id='demo_2',
        schedule_interval=datetime.timedelta(days=1),
        start_date=YESTERDAY) as dag:

    perl = kubernetes_pod_operator.KubernetesPodOperator(
        task_id='first',
        name='first-perl',
        cmds=['perl', '-e', 'print "first"'],
        namespace='default',
        image='perl',
        get_logs=True)

    js = kubernetes_pod_operator.KubernetesPodOperator(
        task_id='second',
        name='second-js',
        cmds=["/bin/bash", "-c",
              "echo \"console.log('second')\" > second.js && node second.js"],
        namespace='default',
        image='node',
        get_logs=True)

    java = kubernetes_pod_operator.KubernetesPodOperator(
        task_id='third',
        name='third-java',
        cmds=["/bin/bash", "-c",
              "echo 'class third{public static void main(String args[]){System.out.println(\"third\");}}' > third.java && javac third.java && java third"],
        namespace='default',
        image='openjdk',
        get_logs=True)

    perl >> js >> java
