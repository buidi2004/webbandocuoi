# Build Stage
FROM node:20-alpine as build

WORKDIR /app

# Build argument for API URL
ARG VITE_API_BASE_URL=https://ivie-backend.onrender.com
ENV VITE_API_BASE_URL=$VITE_API_BASE_URL

# Cache bust - update this to force rebuild: v2025.01.01
ARG CACHEBUST=1

# Copy package files first for better caching
COPY package.json package-lock.json ./

# Install dependencies
RUN npm ci

# Copy source code
COPY . .

# Build the application with env
RUN npm run build

# Production Stage (Nginx)
FROM nginx:alpine

# Copy built assets from build stage
COPY --from=build /app/dist /usr/share/nginx/html

# Copy custom nginx config
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
