# syntax=docker/dockerfile:1.7-labs

FROM node:22-alpine AS build

WORKDIR /app

RUN corepack enable

COPY package.json ./
COPY tsconfig*.json ./
COPY vite.config.ts uno.config.ts vitest.config.ts ./
COPY .eslintrc.cjs ./
COPY env.d.ts ./
COPY index.html ./
COPY public ./public
COPY src ./src
COPY tests ./tests
COPY nginx.conf ./nginx.conf

RUN pnpm install --no-frozen-lockfile
RUN pnpm build

FROM nginx:1.27-alpine AS production

COPY --from=build /app/dist /usr/share/nginx/html
COPY public/favicon.svg /usr/share/nginx/html/favicon.svg
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]


