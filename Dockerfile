FROM python:3.7
USER root

COPY requirements.txt /root/

RUN apt-get update && apt-get upgrade -y
RUN apt-get install -y libgl1-mesa-dev

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r /root/requirements.txt

WORKDIR /root/src

# CMD ["python", "main.py"]