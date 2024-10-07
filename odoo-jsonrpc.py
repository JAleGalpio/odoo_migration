import requests

jsonrpcid = 0
url = "https://demo-28-08-6.adhoc.ar/jsonrpc"
db = "demo-28-08-6"
username = "Chargebee"
password = "Chargebee"
headers = {'Content-Type': 'application/json'}

# Preparar conexión
data = {
    "jsonrpc": "2.0",
    "method": "call",
    "params": {
        "service": "common",
        "method": "login",
        "args": [db, username, password]
    },
    "id": 1
}

# Realizar solicitud HTTP POST
response = requests.post(url, headers=headers, json=data)
result = response.json()

if 'result' in result:
    uid = result['result']
    print(f"Logged in with UID: {uid}")
else:
    print("Failed to log in")
    exit(1)

# SEARCH
query_data = {
    "jsonrpc": "2.0",
    "method": "call",
    "params": {
        "service": "object",
        "method": "execute_kw",
        # args: [db, uid, password, model, method, [domain, offset, limit], {**kwargs}]
        "args": [db, uid, password, 'res.partner', 'search', [[['id', '>', 1]], 0, 10]],
    },
    "id": 2
}

query_response = requests.post(url, headers=headers, json=query_data)
result = query_response.json()
print(result)

# READ
query_data = {
    "jsonrpc": "2.0",
    "method": "call",
    "params": {
        "service": "object",
        "method": "execute_kw",
        # args: [db, uid, password, model, method, [ids, fields], {**kwargs}]
        "args": [db, uid, password, 'res.partner', 'read', [result['result'], ['name']], {'context': {'pricelist': 1}}],
    },
    "id": 2
}

query_response = requests.post(url, headers=headers, json=query_data)
result = query_response.json()
print(result)

# SEARCH-READ
query_data = {
    "jsonrpc": "2.0",
    "method": "call",
    "params": {
        "service": "object",
        "method": "execute_kw",
        # args: [db, uid, password, model, method, [domain, fields, offset, limit], {**kwargs}]
        "args": [db, uid, password, 'res.partner', 'search_read', [[], ['name', 'email'], 0, 10]],
    },
    "id": 2
}

query_response = requests.post(url, headers=headers, json=query_data)
result = query_response.json()

print(result['result'])
