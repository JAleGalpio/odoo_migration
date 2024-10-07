import requests

jsonrpcid = 0
url = "https://demo-28-08-6.adhoc.ar/jsonrpc"
db = "demo-28-08-6"
username = "Chargebee"
password = "Chargebee"
headers = {'Content-Type': 'application/json'}


class Odoo():

    def __init__(self):
        self.jsonrpcid = 0

    def call(self, method: str, service: str, *args):
        self.jsonrpcid += 1

        data = {
            "jsonrpc": "2.0",
            "method": "call",
            "params": {
                "service": service,
                "method": method,
                "args": args
            },
            "id": self.jsonrpcid
        }

        # Realizar solicitud HTTP POST
        response = requests.post(url, headers=headers, json=data)
        result = response.json()

        return result

    def login(self, db: str, username: str, password: str):
        self.db = db
        self.username = username
        self.password = password
        outcome = self.call('login', 'common', self.db, self.username, self.password)
        if 'result' not in outcome:
            raise Exception('Failed to login')
        self.uid = outcome['result']

    def execute(self, *args):
        result = self.call('execute_kw', 'object', self.db, self.uid, self.password, *args)
        r = result.get('result', False)
        if not r:
            print(result)
            raise Exception('Command has failed')
        return r

    def read(self, model: str, ids: list=[], fields: list=[], context: dict={}):
        return self.execute(model, 'read', [ids, fields], {'context': context})

    def search_read(self, model: str, domain: list=[], fields: list=[], offset: int=0, limit: int=10, context: dict={}):
        return self.execute(model, 'search_read', [domain, fields, offset, limit], {'context': context})

    def create(self, model: str, vals_list: list=[], context: dict={}):
        return self.execute(model, 'create', vals_list, {'context': context})

# Crear nueva instancia
odoo = Odoo()

# Realizar login
odoo.login(db, username, password)

# Obtener campos de un modelo y atributos especificos
odoo.execute('res.partner', 'fields_get', [], {'attributes': ['string', 'help', 'type']})


odoo.create('res.partner', [{'name': 'Partner 1', 'vat': '22333444'}])

odoo.execute('account.move', 'action_post', [155])
