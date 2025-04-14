FROM python:3.12-slim

ARG VERSION=latest
ENV VERSION=${VERSION}
RUN echo "Building version ${VERSION}"

WORKDIR /code

# Install dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    curl ca-certificates && \
    rm -rf /var/lib/apt/lists/*

# Install the application dependencies.
RUN --mount=from=ghcr.io/astral-sh/uv:0.6.4,source=/uv,target=/bin/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --all-groups --frozen --no-cache 

ENV PATH="/code/.venv/bin:${PATH}"

# Copy the application into the container.
COPY ./app /code/app
CMD ["/code/.venv/bin/uvicorn", "app.main:app", "--host",  "0.0.0.0", "--port", "8000"]