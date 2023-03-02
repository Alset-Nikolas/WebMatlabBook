FROM python:3.8.10
RUN apt update && apt install -y octave

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /home/matlab_book
COPY requirements.txt /home/matlab_book/

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . /home/matlab_book/

ENV PYTHONPATH "${PYTHONPATH}:/home/matlab_book"



RUN chmod a+x  /home/matlab_book/docker-entrypoint.sh

ENTRYPOINT ["/home/matlab_book/docker-entrypoint.sh"]


