FROM python:3.11 as base
WORKDIR /app
RUN pip install uv
COPY pyproject.toml uv.lock* ./
RUN uv sync
COPY . .

FROM base AS dev
EXPOSE 8000
CMD ["uv", "run", "uvicorn", "app.main:app", "--reload"]

FROM base AS prod
EXPOSE 8000
CMD ["uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0" ,"--port", "8000"]