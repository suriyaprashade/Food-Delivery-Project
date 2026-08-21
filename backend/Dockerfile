FROM node:20-alpine

WORKDIR /app

COPY package*.json ./
RUN npm ci --omit=dev

COPY --chown=node:node . .

RUN mkdir -p /app/uploads && \
    chown -R node:node /app/uploads

USER node

EXPOSE 4000

CMD ["node", "server.js"]
