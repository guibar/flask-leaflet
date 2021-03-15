from random import random
from geopandas import GeoDataFrame
from flask import Flask, request, render_template
from shapely.geometry import Polygon
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.route('/json', methods=['GET', 'POST'])
def add_message():
    data = request.json

    gdf_points = GeoDataFrame.from_features(data["features"])
    polygon: Polygon = gdf_points['geometry'].agg(lambda point: Polygon(point.tolist()))
    gdf_poly = GeoDataFrame([{'geometry': polygon}])

    print(gdf_poly.to_json())
    return gdf_poly.to_json()


@app.route('/random')
def rand():
    return "this was returned: {}".format(random())


if __name__ == '__main__':
    app.run()
