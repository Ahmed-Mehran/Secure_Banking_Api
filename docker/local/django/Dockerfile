FROM python:3.12.2-slim-bookworm AS python

# red mark is for necessary and important commands

# STAGE 1: Build our dependency wheels
FROM python AS python-build-stage

ARG BUILD_ENVIRONMENT=local 

RUN apt-get update && apt-get install --no-install-recommends -y \
    build-essential \
    libpq-dev

COPY ./requirements .

RUN pip wheel --wheel-dir /usr/src/app/wheels \
    -r ${BUILD_ENVIRONMENT}.txt


## In simple terms: the above command creates a folder full of pre-built Python packages(compiled pre installed packages) so that the final Docker image becomes smaller, faster, and doesn’t need to recompile dependencies every time.

## So in this Build stage we are saying choose the build environment as local, then install the necessary tools for compiling and stuff and then compile and store the pre installed files in wheel form in the folder, 
## so that these could be copied and installed during the runtime

# STAGE 2 : Run Stage

FROM python AS python-run-stage

ARG BUILD_ENVIRONMENT=local

ARG APP_HOME=/app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONNUNBUFFERED=1 \
    BUILD_ENV=${BUILD_ENVIRONMENT}

WORKDIR ${APP_HOME}


RUN apt-get update && apt-get install --no-install-recommends -y \
    sudo git bash-completion nano ssh \
    libpq-dev gettext \
    && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
    && rm -rf /var/lib/apt/lists/*


RUN addgroup --system django && \
    adduser --system --ingroup django django && \
    mkdir -p ${APP_HOME}/staticfiles && \
    chown django:django ${APP_HOME}/staticfiles && \
    chmod 775 ${APP_HOME}/staticfiles


COPY --from=python-build-stage /usr/src/app/wheels  /wheels/

# Docker will create /wheels/ in the final stage if it doesn't already exist, and then copy all the wheel files from the build stage's /usr/src/app/wheels into it. So the meaning is: “take the wheels built 
# in the first stage and place them into a /wheels/ directory in this final image” — it's simply a destination path inside the new image.


RUN pip install --no-cache-dir --no-index  --find-links=/wheels/  /wheels/* \
    && rm -rf /wheels/

# Now pip installs packages directly from the wheels folder. There is no downloading, no compiling. This makes install extremely fast. Then the wheels folder is deleted to save space. 
# so in short we first copy the wheel files from build stage from wheel folder and store it inside a new \wheel\ folder inside the final run image, then just install the pre compiled wheel 
# files(requirement.txt in wheel file format) and then delete as we dont need it

COPY --chown=django:django  ./docker/local/django/entrypoint.sh  /entrypoint.sh
COPY --chown=django:django  ./docker/local/django/start.sh  /start.sh


RUN sed -i 's/\r$//g' /entrypoint.sh  /start.sh  && \
    chmod +x /entrypoint.sh  /start.sh


COPY --chown=django:django . ${APP_HOME}
# This finally copies your full Django project code into /app. Ownership is assigned to the django user to avoid root access. Could have written as   COPY . ${APP_HOME}

USER django 

ENTRYPOINT [ "/entrypoint.sh" ] 
## In simple words: the Dockerfile is only for building the image, but when you actually run the container, you often need to execute some setup steps before starting the
#  Django server — like applying migrations, collecting static files, waiting for the database, etc. The ENTRYPOINT is simply a script (a file) that contains all these commands.
#  These commands do not run during image build. They run inside the container, right before the Django server starts. So: the container starts → entrypoint script runs inside 
#  it → migrations/static collection/etc happen inside the container → finally it starts the server. This is exactly why we use an entrypoint.
#  SO IN SHORT, First the image is built, then the container starts, then the entrypoint script runs inside the container, and finally the script starts the Django server.







