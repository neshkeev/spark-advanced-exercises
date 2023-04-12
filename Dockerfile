FROM jupyter/pyspark-notebook:spark-3.2.1

RUN pip install catboost

ENTRYPOINT [ "start.sh", "jupyter", "lab", "--NotebookApp.token=''", "--NotebookApp.password=''" ]
