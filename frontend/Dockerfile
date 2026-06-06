# Etap 1: Budowanie aplikacji (Node.js)
FROM node:20-alpine AS builder

WORKDIR /app

# Kopiujemy TYLKO package.json.
# Celowo ignorujemy package-lock.json wygenerowany na innym systemie operacyjnym,
# aby uniknąć błędów z plikami binarnymi (np. esbuild/vite) na systemie Linux Alpine.
COPY package.json ./
RUN npm install

# Kopiowanie reszty kodu źródłowego
COPY . .

# Wstrzyknięcie adresu backendu podczas budowania aplikacji.
ARG VITE_API_BASE_URL=http://localhost:8000
ENV VITE_API_BASE_URL=$VITE_API_BASE_URL

# Kompilacja aplikacji React/Vite
RUN npm run build

# Etap 2: Serwowanie plików statycznych (Nginx)
FROM nginx:alpine

# Usunięcie domyślnej strony Nginx
RUN rm -rf /usr/share/nginx/html/*

# Skopiowanie zbudowanych plików z Etapu 1
COPY --from=builder /app/dist /usr/share/nginx/html

# Nginx nasłuchuje domyślnie na porcie 80
EXPOSE 80

# Uruchomienie Nginx w tle
CMD ["nginx", "-g", "daemon off;"]
