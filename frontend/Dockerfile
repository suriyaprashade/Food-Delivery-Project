FROM node:20-alpine AS builder

WORKDIR /app

COPY package*.json ./
RUN npm ci

COPY . .
RUN npm run build


FROM nginx:alpine

# Create non-root user
RUN addgroup -S appgroup && \
    adduser -S appuser -G appgroup

# Copy frontend files
COPY --from=builder /app/dist /usr/share/nginx/html

# Give non-root user permission
RUN chown -R appuser:appgroup /usr/share/nginx/html && \
    chown -R appuser:appgroup /var/cache/nginx && \
    chown -R appuser:appgroup /var/log/nginx && \
    touch /var/run/nginx.pid && \
    chown appuser:appgroup /var/run/nginx.pid

# Nginx listens on non-privileged port
RUN sed -i 's/listen       80;/listen       8080;/' /etc/nginx/conf.d/default.conf

USER appuser

EXPOSE 8080

CMD ["nginx", "-g", "daemon off;"]
