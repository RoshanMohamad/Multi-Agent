# Build stage
FROM node:18-alpine AS build

WORKDIR /app

# Install dependencies
COPY package*.json ./
RUN npm ci

# Copy source and build
COPY . .
RUN npm run build

# Production stage
FROM nginx:alpine

# Copy built assets from build stage to nginx serving directory
COPY --from=build /app/dist /usr/share/nginx/html

# Expose port (Nginx default is 80)
EXPOSE 80

# Add custom Nginx config for client-side routing (React Router) if needed
# We'll use the default for now but write it to handle simple routing
RUN echo 'server { \
    listen 80; \
    location / { \
        root /usr/share/nginx/html; \
        index index.html index.htm; \
        try_files $uri $uri/ /index.html; \
    } \
}' > /etc/nginx/conf.d/default.conf

# Start nginx
CMD ["nginx", "-g", "daemon off;"]
