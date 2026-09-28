# Use the official Astral uv image to pull the high-speed binary
FROM ghcr.io/astral-sh/uv:latest AS uv_bin
FROM python:3.11-slim

WORKDIR /app

COPY --from=uv_bin /uv /uvx /bin/
COPY pyproject.toml uv.lock ./

RUN uv sync --frozen --no-cache

COPY . .

EXPOSE 9020

CMD ["uv", "run", "flask", "run", "--host=0.0.0.0", "--port=9020"]
