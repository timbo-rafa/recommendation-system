def get_client_id(client):
    return int(str(client).translate(str.maketrans(dict.fromkeys('.'))))