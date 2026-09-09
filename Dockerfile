# syntax=docker/dockerfile:1

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# GHDL build stage
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
FROM debian:trixie AS ghdl

RUN apt-get update \
 && apt-get install -y --no-install-recommends \
    build-essential \
    gnat \
    llvm-dev \
    clang \
    zlib1g-dev \
    git \
    ca-certificates \
 && rm -rf /var/lib/apt/lists/*

RUN git clone https://github.com/ghdl/ghdl.git /workspace/ghdl --branch v6.0.0 --depth 1
WORKDIR /workspace/ghdl/build

RUN ../configure --with-llvm-config --prefix=/opt/ghdl
RUN make -j"$(nproc)" && make install


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Final stage
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
FROM astral/uv:0.11-python3.11-trixie-slim AS final

# Retrieve ghdl
ENV CC=clang
ENV PATH="/opt/ghdl/bin:${PATH}"
COPY --from=ghdl /opt/ghdl /opt/ghdl

RUN apt-get update \
 && apt-get install -y --no-install-recommends \
    build-essential \
    libgnat-14 \
    libllvm19 \
    zlib1g-dev \
    clang \
    ca-certificates \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /workspace
COPY pyproject.toml uv.lock ./

ENV UV_PROJECT_ENVIRONMENT=/opt/venv
ENV HOME=/tmp
ENV PYTHONDONTWRITEBYTECODE=1

RUN uv sync --locked --no-install-project

# Entrypoint
CMD ["uv", "run", "--frozen", "pytest", "-v", "./tests"]
