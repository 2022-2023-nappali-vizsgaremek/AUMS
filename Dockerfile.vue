FROM node:16

WORKDIR /app
COPY frontend/package*.json ./

RUN npm install
COPY frontend/ ./

RUN npm run build

FROM nginx:1.21
COPY --from=0 /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]