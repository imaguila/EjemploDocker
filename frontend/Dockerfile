# Usamos Nginx super ligero
FROM nginx:alpine
# Borramos la config por defecto
RUN rm /etc/nginx/conf.d/default.conf
# Copiamos nuestra config
COPY nginx.conf /etc/nginx/conf.d/
# Copiamos nuestra web
COPY index.html /usr/share/nginx/html/