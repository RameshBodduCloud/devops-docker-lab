# =============================
# STAGE 1: BUILD
# =============================

FROM node:22-alpine AS builder

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy application files
COPY server.js ./

# Build application
RUN npm run build


# =============================
# STAGE 2: PRODUCTION
# =============================

FROM node:22-alpine AS production

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install production dependencies only
RUN npm install --omit=dev

# Copy application from builder stage
COPY --from=builder /app/dist ./dist

# Expose application port
EXPOSE 3000

# Run as non-root user
USER node

# Start application
CMD ["node", "dist/server.js"]
