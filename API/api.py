import ee
import requests

# Autenticación e inicialización de Earth Engine
ee.Authenticate()
ee.Initialize(project='land-pablo-diez')

# Definir el punto de interés
point = ee.Geometry.Point([-115.814597, 37.238387])

# Obtener la última imagen Sentinel-2 sin nubes (menos del 5%)
image = ee.ImageCollection("COPERNICUS/S2_SR_HARMONIZED") \
    .filterBounds(point) \
    .filterDate('2023-01-01', '2025-03-03') \
    .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 5)) \
    .sort('system:time_start', False) \
    .first()

# Verificar si hay una imagen disponible
if image:
    # Definir la región de interés (buffer de 1 km)
    region = point.buffer(5000).bounds().getInfo()

    # Seleccionar bandas RGB (Rojo, Verde, Azul)
    image = image.select(['B4', 'B3', 'B2'])

    # Obtener la URL de la imagen en PNG
    url = image.getThumbURL({
        'dimensions': '1024x1024',
        'region': region,
        'format': 'png',
        'min': 0,
        'max': 3000
    })

    # Descargar la imagen
    response = requests.get(url)
    if response.status_code == 200:
        with open("satellite_image.png", "wb") as file:
            file.write(response.content)
        print("✅ Imagen descargada como 'satellite_image.png'")
    else:
        print("❌ Error al descargar la imagen")
else:
    print("⚠ No se encontró una imagen sin nubes para esta ubicación.")
