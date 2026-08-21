FROM node:20-alpine AS builder

WORKDIR /app

COPY package*.json ./
RUN npm ci

COPY . .

RUN npm run build

FROM nginx:alpine

RUN addgroup -S nginxgrp && \
    adduser -S -D -H -u 1001 -G nginxgrp nginxuser

COPY --from=builder /app/dist /usr/share/nginx/html

RUN chown -R 1001:1001 /usr/share/nginx/html

USER 1001

EXPOSE 8080

CMD ["nginx", "-g", "daemon off;"]
