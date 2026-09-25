# syntax=docker/dockerfile:1
# ASG-DEVOPS-008/009: Node builds the assets; only nginx and dist reach runtime.
FROM node:22.23.3-alpine3.24 AS builder

WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM nginx:1.27.5-alpine3.21 AS runtime

COPY nginx.conf /etc/nginx/nginx.conf
RUN rm -rf /usr/share/nginx/html/*
COPY --from=builder --chown=nginx:nginx /app/dist/ /usr/share/nginx/html/

USER nginx
EXPOSE 8080
HEALTHCHECK --interval=10s --timeout=3s --start-period=10s --retries=3 \
    CMD ["wget", "-q", "-O", "/dev/null", "http://127.0.0.1:8080/"]

# Bypass the base image's root-oriented entrypoint scripts. nginx runs as PID 1.
ENTRYPOINT ["nginx"]
CMD ["-g", "daemon off;"]
