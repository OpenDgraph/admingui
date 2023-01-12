import requests

class RunDQL:
    def __init__(self, uri, statusCode, headers):
        self.uri = uri
        self.statusCode = statusCode
        self.headers = headers
    
    def run_query(self, query):
        request = requests.post(
            self.uri, json={'query': query}, headers=self.headers)
        if request.status_code == self.statusCode:
            return request.json()
        else:
            raise Exception(
                f"Unexpected status code returned: {request.status_code}")
    
    def run_mutation(self, mutation, variables=None):
        json = {'query': mutation}
        if variables != None:
            json.update({'variables': variables})
        request = requests.post(self.uri, json=json, headers=self.headers)
        if request.status_code == self.statusCode:
            return request.json()
        else:
            raise Exception(
                f"Unexpected status code returned: {request.status_code}")
