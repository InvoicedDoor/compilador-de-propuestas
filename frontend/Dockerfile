FROM node:22 AS build

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .
RUN npx tsc

FROM nginx:stable-alpine

COPY --from=build /app /usr/share/nginx/html

CMD ["nginx", "-g", "daemon off;"]