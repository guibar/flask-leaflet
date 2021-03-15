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
    point_list = [Point(random.uniform(bounds[0], bounds[2]), random.uniform(bounds[1], bounds[3]))
                  for _ in range(nb_points)]

    gdf_points = GeoDataFrame(point_list, columns=['geometry'])
    return gdf_points.to_json()


def get_random_vehicles_from_box(size: int, seed=None, on_node=False) -> Dict[int, Vehicle]:
    random.seed(seed)
    vehicles = {}
    while len(vehicles) < size:
        random_point: Point = OsmGraph().get_random_point_in_boundary()
        (u, v, key, geom) = get_nearest_edge(OsmGraph().graph, (random_point.y, random_point.x),
                                             return_geom=True, return_dist=False)
        if on_node:
            edge_cursor = 0
        else:
            edge_cursor = random.random()
        point_on_edge = geom.interpolate(geom.length * edge_cursor)

        v_id = random.randint(1000, 10000)
        vehicles[v_id] = Vehicle(v_id, point_on_edge.x, point_on_edge.y, u=u, v=v, edge_cursor=edge_cursor)
    return vehicles


@app.route('/random')
def rand():
    return "this was returned: {}".format(random())


if __name__ == '__main__':
    app.run()
