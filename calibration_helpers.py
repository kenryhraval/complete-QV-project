import jsonpickle

def load_payload(calibration_path) -> dict:
    '''Loads the noise model and coupling map from a JSON file created by the calibration notebook.'''

    with open(calibration_path, "r") as f:
        return jsonpickle.decode(f.read())