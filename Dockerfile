# 1. Usar una imagen base oficial de Python (ligera)
FROM python:3.9-slim

# 2. Establecer el directorio de trabajo dentro del contenedor
# (Es como crear una carpeta 'app' dentro del contenedor y entrar en ella)
WORKDIR /app

# 3. Copiar los archivos de tu ordenador al contenedor
# (El primer punto es tu carpeta actual, el segundo es la carpeta /app)
COPY . .

# 4. Instalar las dependencias
RUN pip install -r requirements.txt

# 5. Exponer el puerto 5000 (el que usa Flask)
EXPOSE 5000

# 6. El comando para arrancar la aplicación
CMD ["python", "app.py"]