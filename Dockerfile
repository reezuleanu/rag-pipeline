FROM python:3.11.11 as builder

WORKDIR /app

# install uv
RUN apt-get update && apt-get install -y curl \
  && curl -LsSf https://astral.sh/uv/install.sh | sh \
  && rm -rf /var/lib/apt/lists/*

ENV PATH="/root/.cargo/bin:$PATH"

COPY . /app

# compile project into a python package
RUN uv pip install --no-cache hatchling \
  && python -m build --wheel

FROM python:3.11.11-slim

WORKDIR /app

# copy config file
COPY --from=builder /app/.streamlit .

# install compiled package
COPY --from=builder /app/dist/*.whl .

RUN pip install --no-cache-dir *.whl && rm *.whl

EXPOSE 8501

CMD ["streamlit", "run", "rag_pipeline/demo/app.py", "--server.port=8501", "--server.address=0.0.0.0"]
