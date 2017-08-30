FROM python:3.5.3

ADD . /products

WORKDIR /products
RUN chmod +x /products/run.sh

RUN apt-get update && apt-get install -y \
  netcat

RUN /bin/bash -c "pip3 install -r /products/requirements/base.txt"
#CMD /products/run.sh
