FROM alpine

RUN apk add --no-cache python3 python3-dev gcc git musl-dev postgresql-dev
RUN pip3 install -U pip && pip3 install poetry

WORKDIR /app
COPY . /app

RUN python3 -m venv .venv
ENV PATH=/app/.venv/bin:$PATH
RUN poetry install --no-dev
RUN python3 -m mullemeck create_tables

ENTRYPOINT [ "python3", "-m", "mullemeck", "production" ]

EXPOSE 5000
