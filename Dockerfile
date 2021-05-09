FROM python:3.9

ARG API_KEY
ARG REDIS_HOST

ENV API_KEY=${API_KEY} REDIS_HOST=${REDIS_HOST}

COPY app .
COPY Pipfile .
COPY Pipfile.lock .

RUN pip install pipenv --no-cache-dir && \
    pipenv install --system --deploy && \
    pip uninstall -y pipenv virtualenv-clone virtualenv

#ENTRYPOINT ["/bin/sh", "-c", "while :; do sleep 10; done"]
CMD [ "python", "main.py" ]