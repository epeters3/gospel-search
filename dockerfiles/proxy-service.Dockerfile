FROM node:gallium-bullseye-slim

COPY package.json package.json

RUN npm install

COPY ./gospel_search ./gospel_search

RUN npm run build

ENTRYPOINT ["npm", "run", "start"]
