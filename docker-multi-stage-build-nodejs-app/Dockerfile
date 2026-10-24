# ====================================
# STAGE 1: BUILDER
# ====================================

FROM node:22-alpine AS builder

WORKDIR /app

COPY package*.json ./

RUN npm ci

COPY server.js .


# ====================================
# STAGE 2: PRODUCTION
# ====================================

FROM node:22-alpine AS production

WORKDIR /app

COPY package*.json ./

RUN npm ci --omit=dev

COPY --from=builder /app/server.js ./server.js

EXPOSE 3000

USER node

CMD ["node", "server.js"]
