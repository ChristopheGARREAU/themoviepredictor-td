FROM python:3.7-buster

RUN pip install argparse mysql-connector-python beautifulsoup4 requests python-dotenv
RUN apt-get clean && apt-get update && apt-get install -y locales
RUN echo 'fr_FR.UTF-8 UTF-8' >> /etc/locale.gen 
RUN echo 'fr_FR ISO-8859-1' >> /etc/locale.gen
RUN echo 'en_US ISO-8859-1 ' >> /etc/locale.gen 
RUN echo 'en_US.UTF-8 UTF-8' >> /etc/locale.gen
RUN locale-gen

COPY . /usr/src/themoviepredictor

WORKDIR /usr/src/themoviepredictor

CMD python /usr/src/themoviepredictor/app.py import --api omdb --imdbId tt0499549
