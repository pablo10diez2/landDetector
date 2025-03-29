import ee
import requests
import os  # To open the image automatically


def authenticate_earth_engine():
    
    #Authenticate and initialize Earth Engine
    ee.Authenticate()
    ee.Initialize(project='land-pablo-diez')



def get_latest_satellite_image(lat, lon):
    
    point = ee.Geometry.Point([lon, lat])

    # Filter for the latest image with <5% cloud coverage
    image = ee.ImageCollection("COPERNICUS/S2_SR_HARMONIZED").filterBounds(point) \
        .filterDate('2023-01-01', '2025-03-03') \
        .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 5)) \
        .sort('system:time_start', False) \
        .first()

    if image:
        return image, point
    else:
        return None, None



def download_image(image, point, filename):

    # Create the APIphotos directory if it doesn't exist
    folder_path = "APIphotos"
    os.makedirs(folder_path, exist_ok=True)

    # Full path for saving the image
    file_path = os.path.join(folder_path, filename)

    # Define region and select RGB bands
    region = point.buffer(5000).bounds().getInfo()
    image = image.select(['B4', 'B3', 'B2'])

    # Get the image URL
    url = image.getThumbURL({'dimensions': '1024x1024', 'region': region, 'format': 'png', 'min': 0, 'max': 3000})

    # Download the image
    response = requests.get(url)

    if response.status_code == 200:

        with open(file_path, "wb") as file:

            file.write(response.content)

        print(f"✅ Image saved as '{file_path}'")

        # Open the image automatically
        os.system(f"xdg-open {file_path}") 
       
    else:
        print("❌ Error downloading the image.")



def main():
    
    authenticate_earth_engine()

    # Get user input
    lat = float(input("Enter latitude: "))
    lon = float(input("Enter longitude: "))
    filename = input("Enter filename (❌ .PNG/.JPG ...): ") + ".png"

    # Get the latest cloud-free image
    image, point = get_latest_satellite_image(lat, lon)

    if image:

        print(f"✅ Found a cloud-free image for {lat}, {lon}. Downloading...")

        download_image(image, point, filename)

    else:
        print("⚠ No cloud-free images found for this location.")




if __name__ == "__main__":
    main()

    