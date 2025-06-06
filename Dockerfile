FROM python:3.11.11 as builder

WORKDIR /app

# install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

RUN python -m venv /venv
ENV PATH="/venv/bin:$PATH"

COPY . /app

# compile project into a python package
RUN uv pip install --no-cache hatchling build \
  && python -m build --wheel

FROM python:3.11.11-slim

WORKDIR /app

# copy config file
COPY --from=builder /app/.streamlit ./.streamlit

# install compiled package
COPY --from=builder /app/dist/*.whl .

# update keys
RUN apt-get update && apt-get install -y --no-install-recommends \
    gnupg ca-certificates

RUN pip install --no-cache-dir *.whl && rm *.whl
RUN playwright install
RUN playwright install-deps

EXPOSE 8501

COPY --from=builder /app/rag_pipeline/demo/app.py /app/demo/app.py

CMD ["streamlit", "run", "demo/app.py", "--server.port=8501", "--server.address=0.0.0.0"]
