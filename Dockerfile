FROM node:14-alpine3.12 AS build_stage
WORKDIR /
COPY package.json package-lock.json ./
RUN npm install
COPY src ./src
COPY public ./public
RUN npm run build

FROM nginx:alpine
COPY --from=build_stage /build/ /usr/share/nginx/html
COPY nginx/nginx.conf /etc/nginx/conf.d/default.conf
