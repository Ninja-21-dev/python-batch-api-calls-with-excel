import http.client

def connect_api(payload):
    conn = http.client.HTTPSConnection("api.aceservices.com")
    
    headers = {
        'X-IBM-Client-Id': "REPLACE_CLIENT_ID",
        'X-IBM-Client-Secret': "REPLACE_THIS_SECRET_TOKEN",
        'content-type': "application/json",
        'accept': "application/json"
        }

    conn.request("POST", "/qa/ShipEstimate", payload, headers)

    res = conn.getresponse()
    data = res.read()

    return data.decode("utf-8")




def connect_api_capsule(payload, sku, qty):
    conn = http.client.HTTPSConnection("api.aceservices.com")
    

    headers = {
        'X-IBM-Client-Id': "REPLACE_CLIENT_ID",
        'X-IBM-Client-Secret': "REPLACE_THIS_SECRET_TOKEN",
        'content-type': "application/json",
        'accept': "application/json"
        }

    conn.request("POST", "/qa/ShipEstimate", payload, headers)

    res = conn.getresponse()
    data = res.read()

    return {
        "data": data.decode('utf-8'),
        "qty": qty,
        "sku": sku
    }
