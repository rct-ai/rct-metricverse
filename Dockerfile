# app/Dockerfile

FROM python:3.9-slim

EXPOSE 8501

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*

#RUN mkdir /root/.ssh/
#
## Copy over private key, and set permissions
## Warning! Anyone who gets their hands on this image will be able
## to retrieve this private key file from the corresponding image layer
#ADD id_rsa /root/.ssh/id_rsa
#
## Create known_hosts
#RUN touch /root/.ssh/known_hosts
## Add bitbuckets key
#RUN ssh-keyscan github.com >> /root/.ssh/known_hosts

#RUN git clone git@github.com:rct-ai/rct-metricverse.git .

COPY ./ .

RUN pip3 install -r requirements.txt

ENTRYPOINT ["streamlit", "run", "📖_About.py", "--server.port=8501", "--server.address=0.0.0.0"]