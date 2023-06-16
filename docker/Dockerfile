FROM python:3.10.5-slim-bullseye

RUN groupadd -g 1337 app && \
    useradd -m -d /opt/app -u 1337 -g app app

ENV PYTHONPATH=${PYTHONPATH}:${PWD}

RUN pip3 install poetry
WORKDIR /temp
ADD pyproject.toml /temp/pyproject.toml
RUN poetry config virtualenvs.create false

ARG INSTALL_DEV=false
ARG INTERNAL_PORT=80
RUN bash -c "if [ $INSTALL_DEV == 'true' ] ; then poetry install --no-root ; else poetry install --no-root --no-dev ; fi"

USER app
WORKDIR /opt/app
ENV PATH /opt/app/.local/bin:$PATH

EXPOSE $INTERNAL_PORT

COPY --chown=app:app . /opt/temp
RUN if [ "$INSTALL_DEV" = "false" ]; then cp -r /opt/temp/. /opt/app; fi

ADD --chown=app:app scripts/dev /usr/local/bin/
RUN ["chmod", "+x", "/usr/local/bin/dev"]

ADD --chown=app:app scripts/deployment/core.sh /
RUN ["chmod", "+x", "/core.sh"]

ENTRYPOINT ["/core.sh"]
