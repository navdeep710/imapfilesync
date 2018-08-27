FROM python:3.5
ADD . /
RUN mkdir -p /tmp/watermark
RUN mkdir -p /tmp/attachments
RUN pip install -r requirements.txt


