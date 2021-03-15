import random

from geopandas import GeoDataFrame
from flask import Flask, request, render_template
from shapely.geometry import Polygon, Point
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.route('/json', methods=['GET', 'POST'])
def add_message():
    data = request.json

    gdf_points: GeoDataFrame = GeoDataFrame.from_features(data["features"])
    polygon: Polygon = gdf_points['geometry'].agg(lambda point: Polygon(point.tolist()))
    gdf_poly = GeoDataFrame([{'id': 1, 'geometry': polygon}])

    print(gdf_poly.to_json())
    return gdf_poly.to_json()


@app.route('/points', methods=['GET'])
def get_points():
    nb_points = 10
    bounds = [7.723255, 48.573153, 7.785568, 48.596092]
    point_list = [('True', Point(random.uniform(bounds[0], bounds[2]), random.uniform(bounds[1], bounds[3])))
                  for _ in range(nb_points)]

    gdf_points = GeoDataFrame(point_list, columns=['draggable', 'geometry'])
    return gdf_points.to_json()


@app.route('/random')
def rand():
    return "this was returned: {}".format(random.random())


if __name__ == '__main__':
    app.run()
