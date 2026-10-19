FROM python:3.15-slim-trixie

COPY --from=ghcr.io/astral-sh/uv:0.13.1 /uv /usr/local/bin/uv

# tkinter と仮想ディスプレイ、ブラウザ表示に必要なパッケージをインストールします。
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        libtk8.6 fonts-dejavu-core xvfb xauth x11vnc websockify \
    && rm -rf /var/lib/apt/lists/*

# noVNC は静的ファイルだけ使います。 Debian の novnc パッケージは nodejs まで入るので upstream から取得します。
ADD --checksum=sha256:b1003a11b6e6e8d8f7f5e5586daae7f8ca651d8aee0aa155ff9ac841c48f52c6 \
    https://github.com/novnc/noVNC/archive/refs/tags/v1.7.0.tar.gz /tmp/novnc.tar.gz
RUN mkdir /opt/novnc \
    && tar -xzf /tmp/novnc.tar.gz -C /opt/novnc --strip-components=1 \
    && rm /tmp/novnc.tar.gz

ENV UV_PROJECT_ENVIRONMENT=/opt/venv \
    UV_PYTHON_DOWNLOADS=never \
    UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    PATH=/opt/venv/bin:$PATH

WORKDIR /app
COPY pyproject.toml uv.lock ./
RUN uv sync --locked

# Xvfb は root 以外だと X ソケット用ディレクトリを作れず ERROR を出すので、先に作っておきます。
RUN useradd --create-home app && chown app:app /app && mkdir -m 1777 /tmp/.X11-unix
COPY --chown=app:app . .
USER app

EXPOSE 6080
CMD ["docker/start-gui.sh"]
