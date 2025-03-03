import ee
import geemap

# Autenticar y inicializar Earth Engine
ee.Authenticate()
ee.Initialize(project='land-pablo-diez')

# Definir el punto de coordenadas
point = ee.Geometry.Point(40.274290, -2.930503)

# Obtener la última imagen de la colección de Landsat 9 (LC09)
image_collection = ee.ImageCollection('LANDSAT/LC09/C02/T1') \
    .filterBounds(point) \
    .filterDate('2021-01-01', '2025-03-03') \
    .sort('system:time_start', False)

# Verificar cuántas imágenes están disponibles en la colección
image_count = image_collection.size().getInfo()
print(f"Imágenes disponibles: {image_count}")

# Si hay imágenes disponibles, obtener la primera imagen
if image_count > 0:
    image = image_collection.first()
    print("Imagen obtenida con éxito.")
    
    # Definir la región (buffer de 1 km alrededor del punto)
    region = point.buffer(1000).bounds()

    # Descargar la imagen usando geemap
    map = geemap.Map()
    map.centerObject(point, 10)  # Centrar el mapa en el punto de interés
    map.addLayer(image.clip(region), {}, 'image')  # Añadir la capa de imagen al mapa
    map.save("satellite_image.html")  # Guardar el mapa como archivo HTML para visualizar en tu navegador

    # Exportar la imagen a Google Drive
    task = ee.batch.Export.image.toDrive(
        image=image,
        description='latest_satellite_image',
        fileFormat='GeoTIFF',
        region=region,  # Usamos la geometría directamente
        scale=30,  # Resolución espacial
        folder='your_folder'  # (opcional) Especifica la carpeta en Google Drive
    )

    # Iniciar la tarea de exportación
    task.start()

    # Comprobar el estado de la tarea
    import time
    while task.active():
        print("Exportando imagen...")
        time.sleep(10)  # Espera 10 segundos antes de comprobar el estado nuevamente

    print("Tarea completada:", task.status())
else:
    print("No se encontraron imágenes en la colección con los filtros especificados.")
