FROM python:3.8-slim

ARG PYTHON_VERSION=3.8
RUN apt-get update && apt-get install  -y --no-install-recommends \
    nodejs \
    curl \
    git \
    npm && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN node --version
ENV LANG=C.UTF-8

RUN pip --no-cache-dir install \
      jupyter \
      ipywidgets \
      jupyterlab \
      cython \
      jupyter-lab-serverless \
      jupyterlab_code_formatter \
      jupyterlab-snippets \
      sqlalchemy

RUN jupyter labextension install \
    @jupyter-widgets/jupyterlab-manager \
    @u2takey/jupyter-lab-serverless \
    @jupyterlab/toc \
    @krassowski/jupyterlab_go_to_definition \
    @ryantam626/jupyterlab_code_formatter

ARG CACHEBUST=1 
RUN pip --no-cache-dir install --upgrade jupyter-lab-serverless \
    requests

EXPOSE 8888
WORKDIR /opt/app/data
RUN mkdir -p /opt/app/data
CMD jupyter lab --ip=* --port=8888 --no-browser --allow-root
