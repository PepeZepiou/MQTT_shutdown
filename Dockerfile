FROM python:3.12-lite

RUN pip install -r /scripts/requirements.txt

CMD script.py
