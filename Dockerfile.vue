FROM node:16

# App directory
WORKDIR /app
COPY frontend/package*.json ./

# Install and build
RUN npm install
COPY frontend/ ./
RUN npm run build

# Web server
FROM nginx:1.21
COPY --from=0 /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Port, run command
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]