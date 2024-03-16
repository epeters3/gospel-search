FROM node:20.11.1-bookworm-slim

COPY package.json package.json

RUN npm install

COPY ./gospel_search ./gospel_search

RUN npm run build

ENTRYPOINT ["npm", "run", "start"]
