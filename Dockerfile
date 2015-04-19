############################################################
# Docker for eliasson/boutique
############################################################

FROM ubuntu:precise

RUN apt-get update

RUN apt-get install -y tar git curl vim wget dialog net-tools build-essential

RUN apt-get install -y python python-dev python-distribute python-pip

# Copy the application folder inside the container
ADD . /boutique

# Get pip to download and install requirements:
RUN pip install -r /boutique/requirements/development.txt

RUN python /boutique/boutique/manage.py syncdb --migrate --noinput --settings=boutique.settings.development
RUN python /boutique/boutique/manage.py loaddata /boutique/fixtures/catalogue.json --settings=boutique.settings.development

CMD python /boutique/boutique/manage.py runserver 0.0.0.0:8000 --settings=boutique.settings.development
