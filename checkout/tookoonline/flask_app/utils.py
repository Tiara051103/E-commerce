from pydantic import ValidationError

def validasi(model, sumber_data):
    try:
        return model(**sumber_data)
    except ValidationError as e:
        return None, e.errors()