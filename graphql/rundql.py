#
#  Copyright 2023 Dgraph Labs, Inc. and Contributors
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#

import requests


class RunDQL:
    def __init__(self, uri, statusCode, headers):
        self.uri = uri
        self.statusCode = statusCode
        self.headers = headers

    def run_query(self, query, variables=None):
        json = {'query': query}
        if variables != None:
            json.update({'variables': variables})

        request = requests.post(
            self.uri, json=json, headers=self.headers)

        if request.status_code == self.statusCode:
            return request.json()
        else:
            raise Exception(
                f"Unexpected status code returned: {request.status_code}")
