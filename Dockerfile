# CPU-only LoRR 2026 official Start-Kit, build from a pinned upstream commit.
FROM python:3.11-slim-bookworm

ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y --no-install-recommends \
    git ca-certificates cmake build-essential pkg-config libboost-all-dev \
    && rm -rf /var/lib/apt/lists/*

# Official Start-Kit v3.1.0 requires Python >=3.11 and pybind11 >=3.0.1.
RUN python -m pip install --no-cache-dir pybind11==3.0.1

ARG LORR_COMMIT=9bc75d9dd9883de049294ab2981bf325bbe19d49
RUN git clone https://github.com/MAPF-Competition/Start-Kit.git /opt/lorr-start-kit \
    && git -C /opt/lorr-start-kit checkout --detach "${LORR_COMMIT}" \
    && git -C /opt/lorr-start-kit rev-parse HEAD > /opt/lorr-source-commit.txt

# Disable the official optional test targets only for the first smoke-build.
# Compile with two jobs to keep memory usage manageable on 16 GB laptops.
RUN cmake -S /opt/lorr-start-kit -B /opt/lorr-start-kit/build \
      -DCMAKE_BUILD_TYPE=Release \
      -DBUILD_TESTS=OFF \
      -Dpybind11_DIR="$(python -m pybind11 --cmakedir)" \
    && cmake --build /opt/lorr-start-kit/build --parallel 2

WORKDIR /workspace
ENTRYPOINT ["/opt/lorr-start-kit/build/lifelong"]
