# Etap 1: Budowanie aplikacji (Node.js)
FROM node:20-alpine AS builder

WORKDIR /app

# Kopiowanie plików konfiguracyjnych i instalacja zależności
COPY package*.json ./
RUN npm install

# Kopiowanie kodu źródłowego
COPY . .

# Wstrzyknięcie adresu backendu podczas budowania aplikacji.
# Dzięki temu React wie, gdzie wysyłać zapytania API w wersji produkcyjnej.
ARG VITE_API_BASE_URL=http://localhost:8000
ENV VITE_API_BASE_URL=$VITE_API_BASE_URL

# Kompilacja aplikacji React/Vite do czystego HTML/CSS/JS (katalog dist/)
RUN npm run build

# Etap 2: Serwowanie plików statycznych (Nginx)
FROM nginx:alpine

# Usunięcie domyślnej strony Nginx
RUN rm -rf /usr/share/nginx/html/*

# Skopiowanie zbudowanych plików z Etapu 1 do serwera Nginx
COPY --from=builder /app/dist /usr/share/nginx/html

# Nginx nasłuchuje domyślnie na porcie 80
EXPOSE 80

# Uruchomienie Nginx w tle
CMD ["nginx", "-g", "daemon off;"]
