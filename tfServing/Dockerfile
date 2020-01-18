FROM python:3.7.6-buster

ENV INSTALL_PATH /tfserving
RUN mkdir $INSTALL_PATH
WORKDIR $INSTALL_PATH

ENV PYTHONUNBUFFERED 1

RUN echo "deb [arch=amd64] http://storage.googleapis.com/tensorflow-serving-apt stable tensorflow-model-server tensorflow-model-server-universal" | tee /etc/apt/sources.list.d/tensorflow-serving.list && \
    curl https://storage.googleapis.com/tensorflow-serving-apt/tensorflow-serving.release.pub.gpg | apt-key add -
RUN apt update

RUN apt-get install tensorflow-model-server

# tail server.log

COPY resnet resnet

CMD tensorflow_model_server \
    --rest_api_port=8501 \
    --model_name=resnet \
    --model_base_path="/resnet" >server.log 2>&1