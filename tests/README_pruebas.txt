PRUEBAS AUTOMATIZADAS (Selenium) - como ejecutarlas en Windows

1) Instalar dependencias (una sola vez):
     pip install -r tests\requirements.txt

2) Probar contra la app desplegada en Render:
     set BASE_URL=https://TU-APP.onrender.com
     pytest tests -v

   (Opcional) Ver el navegador mientras corre:
     set HEADLESS=0

Las capturas de evidencia se guardan en la carpeta "evidencias".
