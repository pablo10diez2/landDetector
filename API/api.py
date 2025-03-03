import ee
import requests
from PIL import Image

ee.Authenticate()
ee.Initialize(project = 'land-pablo-diez')

point = ee.Geometry.Point([40.65724, -4.69951])

image = ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED') \
    .filterBounds(point) \
    .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 5)) \
    .filter(ee.Filter.lt('MEAN_SOLAR_ZENITH_ANGLE', 70)) \
    .sort('system:time_start', False).first()

if(image):
    region = point.buffer(10000).bounds()

    image = image.select(['B4', 'B3', 'B2'])

    url = image.getThumbURL({
        'dimensions': '1024x1024',
        'region': region.getInfo(),
        'format':'png',
        'min':0,
        'max':30000
    })

    response = requests.get(url)
    if(response.status_code == 200):
        with open("satellite_image.png", "wb") as file:
            file.write(response.content)

    else:
        print("Error con la imagen")
else:
    print("Error 2")