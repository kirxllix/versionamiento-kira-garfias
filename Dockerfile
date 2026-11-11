# Imagen base ligera: servidor web Nginx sobre Alpine Linux
FROM nginx:alpine

# Copiar solo los archivos de la aplicacion al directorio publico de Nginx
COPY index.html styles.css functions.js /usr/share/nginx/html/

# Exponer el puerto 80 para el trafico web
EXPOSE 80
