from serialize import receive_info


def add_routes(app):
    app.add_url_rule("/", view_func=receive_info, methods=["POST", "GET"])
