FROM node:14-alpine3.12
COPY package.json package-lock.json ./
WORKDIR ./
RUN npm install
COPY src ./src
COPY public ./public
RUN npm run build
RUN npm run start
