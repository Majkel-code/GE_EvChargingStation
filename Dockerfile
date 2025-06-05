# syntax=docker/dockerfile:1.4

# -------- Base Stage --------
FROM python:3.10-slim as base

ARG VERSION=0.0.0
ENV VERSION=${VERSION}

WORKDIR /app
COPY requirements.txt .

RUN apt-get update && apt-get install -y \
    build-essential \
    python3-dev \
    python3-pip \
    fakeroot \
    dpkg-dev \
    nodejs \
    npm && \
    pip install --upgrade pip && \
    pip install -r requirements.txt && \
    pip install pyinstaller

# -------- Build Charger App --------
FROM base as build-charger
ARG VERSION
ENV VERSION=${VERSION}
COPY . /app

RUN pyinstaller /app/.builders_cfg/pyinstaller/charger_app.spec

RUN mkdir -p /deb-package/home/ge_run && \
    cp /app/BUILDER/charger/charger-app /deb-package/home/ge_run/ && \
    mkdir -p /deb-package/DEBIAN && \
    echo "Package: charger-app" > /deb-package/DEBIAN/control && \
    echo "Version: ${VERSION}" >> /deb-package/DEBIAN/control && \
    echo "Architecture: arm64" >> /deb-package/DEBIAN/control && \
    echo "Maintainer: Michal Kotlowski <michalkotlowski7@gmail.com>" >> /deb-package/DEBIAN/control && \
    echo "Description: Charger App" >> /deb-package/DEBIAN/control

RUN dpkg-deb --build /deb-package "/app/charger-app_${VERSION}_arm64.deb"

# -------- Build Vehicle App --------
FROM base as build-vehicle
ARG VERSION
ENV VERSION=${VERSION}
COPY . /app

RUN pyinstaller /app/.builders_cfg/pyinstaller/vehicle_app.spec

RUN mkdir -p /deb-package/home/ge_run && \
    cp /app/BUILDER/vehicle/vehicle-app /deb-package/home/ge_run/ && \
    mkdir -p /deb-package/DEBIAN && \
    echo "Package: vehicle-app" > /deb-package/DEBIAN/control && \
    echo "Version: ${VERSION}" >> /deb-package/DEBIAN/control && \
    echo "Architecture: arm64" >> /deb-package/DEBIAN/control && \
    echo "Maintainer: Michal Kotlowski <michalkotlowski7@gmail.com>" >> /deb-package/DEBIAN/control && \
    echo "Description: Vehicle App" >> /deb-package/DEBIAN/control

RUN dpkg-deb --build /deb-package "/app/vehicle-app_${VERSION}_arm64.deb"

# -------- Build Display App (Electron Forge) --------
FROM node:18-slim as build-display

ARG VERSION=1.0.0
ENV VERSION=$VERSION

WORKDIR /app

# Install required tools for building .deb packages
RUN apt-get update && apt-get install -y \
    fakeroot \
    dpkg-dev 


# Copy only package.json and package-lock.json first to leverage Docker caching
COPY DISPLAY/package.json DISPLAY/package-lock.json /app/

# Install dependencies
RUN npm install
RUN npm install --save-dev electron-forge
RUN npm install --save-dev @electron-forge/cli
RUN apt-get install rpm -y
# Copy the rest of the Electron app files
COPY DISPLAY/ /app


# Build the Electron app using Electron Forge
RUN npm run make


# The final Electron package (e.g., .deb) will be in /app/out/make
# RUN mkdir -p /deb-package && \
#     cp /app/out/make/deb/arm64/*.deb /deb-package/


# -------- Final Stage --------
FROM base as final

ARG VERSION
ENV VERSION=${VERSION}

WORKDIR /app
RUN mkdir -p /app/deb-packages

COPY --from=build-charger /app/charger-app_${VERSION}_arm64.deb /app/deb-packages/
COPY --from=build-vehicle /app/vehicle-app_${VERSION}_arm64.deb /app/deb-packages/
COPY --from=build-display /app/out/make/deb/arm64/*.deb /app/deb-packages/