FROM python:2-alpine3.6
LABEL maintainer=<kreczko@cern.ch>

RUN apk --no-cache --update-cache add gcc gfortran python python-dev py-pip build-base wget freetype-dev libpng-dev openblas-dev
RUN ln -s /usr/include/locale.h /usr/include/xlocale.h

ADD requirements.txt /tmp/requirements.txt
RUN pip install -U pip
RUN pip install --no-cache-dir -r /tmp/requirements.txt

ADD ./webapp /opt/webapp/
WORKDIR /opt/webapp
EXPOSE 5000

ENV PORT 5000
CMD ["python", "app.py"]
