# Use Python 3.12+ slim image as base
FROM python:3.12-slim

# Install uv globally for all users
RUN pip install uv

# --- Root User Setup ---
# Create a non-root user, group, and home directory for security
RUN addgroup --system appgroup && \
    adduser --system --ingroup appgroup --home /home/appuser appuser

# Create and set permissions for the UV cache directory
# This allows caching to work correctly for the non-root user
ENV UV_CACHE_DIR=/home/appuser/.cache/uv
RUN mkdir -p $UV_CACHE_DIR && chown -R appuser:appgroup /home/appuser

# --- Switch to Non-Root User ---
# All subsequent commands will be run as 'appuser'
USER appuser

# Set working directory. This directory will be created with 'appuser' as the owner.
WORKDIR /app

# Copy dependency files. The '--chown' flag ensures correct ownership.
COPY --chown=appuser:appgroup pyproject.toml uv.lock ./

# Install dependencies.
# Because we are now 'appuser', the .venv created by 'uv' will be owned by 'appuser'.
RUN uv sync --frozen

# Copy source code with correct ownership
COPY --chown=appuser:appgroup weather.py ./

# --- Runtime Configuration ---
# Set FastMCP host to bind to all interfaces for Docker
ENV FASTMCP_HOST=0.0.0.0

# Expose port (adjust if your server uses a different port)
EXPOSE 8000

# Run the MCP server
CMD ["uv", "run", "python", "weather.py"]