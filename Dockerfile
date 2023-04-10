FROM jupyter/pyspark-notebook

USER jovyan

ENV EDITOR=vim

RUN pip install --upgrade pip && \
  pip install bash_kernel && \
  python -m bash_kernel.install

RUN ssh-keygen -t rsa -P '' -f ~/.ssh/id_rsa

COPY bin/pyspark /bin/entrypoint

ENTRYPOINT [ "/bin/entrypoint" ]
