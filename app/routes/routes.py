from app.routes.serialize import receive_info


def add_routes(app):
    app.add_url_rule("/receive_info/", view_func=receive_info, methods=["POST", "GET"])
