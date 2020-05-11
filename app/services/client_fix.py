def get_client_id(client):
    """O formato da identificacao do cliente nao equivale a nenhum dos campos do cliente.
       Adaptamos o campo "cliente" existente na ordem para comparar com o id do cliente.
       
       e.g.:

       ordem: {\n
           ...

           "cliente": "000.000.000.01",
           ...
       }

        removemos os pontos e convertemos em inteiro para pegar id 1 do cliente.

    Arguments:
        client {string} -- campo cliente da ordem como descrito acima

    Returns:
        [int] -- id do cliente
    """    
    return int(str(client).translate(str.maketrans(dict.fromkeys('.'))))