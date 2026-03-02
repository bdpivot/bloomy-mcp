FROM python:3.12-slim

WORKDIR /app

# Install dependencies first for better layer caching
COPY pyproject.toml setup.py ./
COPY src/ src/
RUN pip install --no-cache-dir .

# Default to streamable-http for container deployments
ENV MCP_TRANSPORT=streamable-http
ENV HOST=0.0.0.0
ENV PORT=8000

EXPOSE 8000

CMD ["bloomy-server"]
