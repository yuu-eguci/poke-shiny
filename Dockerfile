FROM python:3.15-slim-trixie

COPY --from=ghcr.io/astral-sh/uv:0.13.1 /uv /usr/local/bin/uv

# tkinter と仮想ディスプレイ、ブラウザ表示に必要なパッケージをインストールします。
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        libtk8.6 fonts-dejavu-core xvfb xauth x11vnc novnc websockify \
    && rm -rf /var/lib/apt/lists/*

ENV UV_PROJECT_ENVIRONMENT=/opt/venv \
    UV_PYTHON_DOWNLOADS=never \
    UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    PATH=/opt/venv/bin:$PATH

WORKDIR /app
COPY pyproject.toml uv.lock ./
RUN uv sync --locked

RUN useradd --create-home app && chown app:app /app
COPY --chown=app:app . .
USER app

EXPOSE 6080
CMD ["docker/start-gui.sh"]
