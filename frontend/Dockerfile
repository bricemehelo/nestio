# frontend/Dockerfile
#
# PURPOSE: Builds the React frontend into a Docker container.
# Two stage build:
# Stage 1 — Node: installs dependencies and builds the production bundle
# Stage 2 — Nginx: serves the built static files efficiently
#
# WHY TWO STAGES: The Node image is large (~1GB). We only need it to build.
# The final image uses Nginx (~50MB) to serve the static files — much smaller.

# ── Stage 1: Build ────────────────────────────────────────────────────────────
FROM node:20-slim AS builder

WORKDIR /app

# Copy package files first for layer caching
COPY package*.json

# Install all dependencies including devDependencies needed for the build
RUN npm ci

# Copy source code
COPY . .

# Build the production bundle — outputs to /app/dist
RUN npm dun build

# ── Stage 2: Serve ────────────────────────────────────────────────────────────
FROM nginx:alpine

# Copy the built files from Stage 1 into Nginx's serve directory
COPY --from=builder /app/dist /usr/share/nginx/html

# Copy custom Nginx config — needed for React Router to work correctly
# Without this, refreshing any non-root URL returns 404
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]

