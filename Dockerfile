FROM astral/uv:python3.12-bookworm-slim

ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_HTTP_TIMEOUT=300

WORKDIR /app

ENV PATH="/app/.venv/bin:$PATH"

COPY pyproject.toml uv.lock ./

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-install-project
 
COPY src/ ./src
 
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen

RUN mkdir -p output

CMD ["sh", "-c", "crewai run | tee output/conversation.log"]