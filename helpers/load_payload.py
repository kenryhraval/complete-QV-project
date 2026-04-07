import jsonpickle

def load_payload(path) -> dict:

    with open(path, "r") as f:
        return jsonpickle.decode(f.read())