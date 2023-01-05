import shapefile
import psycopg2
import os,json
import subprocess

# Connect to the database
conn = psycopg2.connect(
    host=os.environ.get("DB_HOST_WEBGIS"), 
    port=5432, 
    database=os.environ.get('DB_NAME_WEBGIS'),
    user=os.environ.get('DB_USER_WEBGIS'), 
    password=os.environ.get('DB_PASSWORD_WEBGIS')
    )


def send_to_postgis(file):
    # Read the shapefile
    file = "myfile.shp"
    sf = shapefile.Reader()

    # Get the shapefile's field names
    fields = [field[0] for field in sf.fields[1:]]

    # Get the shapefile's records
    records = sf.records()

    # Get the shapefile's shapes
    shapes = sf.shapes()

    # Iterate over the shapes and records, and insert them into the database
    for shape, record in zip(shapes, records):
        # Get the shape's coordinates
        coords = shape.points

        # Create a geojson feature from the shape and record
        feature = {
            "type": "Feature",
            "properties": dict(zip(fields, record)),
            "geometry": {
                "type": "MultiPolygon",
                "coordinates": [[[(x, y) for x, y in coords]]]
            }
        }

        # Insert the feature into the database
        cursor = conn.cursor()
        cursor.execute("INSERT INTO mytable (geom, properties) VALUES (ST_SetSRID(ST_GeomFromGeoJSON(%s), 4326), %s)", 
        (
        json.dumps(feature), 
        json.dumps(feature["properties"])
        )
        )
        conn.commit()

def send_to_postgis(file,table_name):
    file = "myfile.shp"

    host=os.environ.get("DB_HOST_WEBGIS")
    database=os.environ.get('DB_NAME_WEBGIS')
    user=os.environ.get('DB_USER_WEBGIS')
    password=os.environ.get('DB_PASSWORD_WEBGIS')

    db_conn = f"host='{host}' port='5432' dbname='{database}' user='{user}' password='{password}'"

    subprocess.call(
        f"ogr2ogr -f 'PostgreSQL' PG:'{db_conn}' {file} -nln {table_name} -overwrite", 
        shell=True
    )