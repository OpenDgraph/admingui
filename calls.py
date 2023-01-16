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

from graphql.rundql import RunDQL
import graphql.readgql as readgql
import arguments as args


class MakeCall:
    def __init__(self, path, variables=None, addr=None):
        self.addr = addr
        self.query = readgql.GetGQL(path).read_gql_file()
        self.variables = variables
        self.headers = {"Content-Type": "application/json",
                        "X-Dgraph-AccessToken": args.arguments.token}

    def make_call(self):
        tree = self.query.split("\n")
        for i in range(len(tree)):
            tree[i] = tree[i].replace('\n', '').replace(
                ' ', '').replace('}', '').replace('{', '')
        tree = list(filter(None, tree))
        if len(tree) > 2:
            while "mutation" in tree[0] or "input" in tree[0] or "filter" in tree[0] or "response" in tree[0] or ")" in tree[0] or tree[0].startswith("#"):
                tree.pop(0)
        try:
            rungql = RunDQL(self.addr, 200, self.headers)
        except NameError:
            error = f"Something else went wrong: {NameError}"
            self.insert_text_event(error)
        except Exception as e:
            error = f"Something else went wrong: {e}"
            self.insert_text_event(error)
        if "mutation" not in self.query:
            run_dql = rungql.run_query(self.query)
        else:
            if "login(userId" in self.query:
                self.query = self.query.replace(
                    "USERIDHERE", str(args.arguments.username))
                self.query = self.query.replace(
                    "XXXX", str(args.arguments.password))
                self.query = self.query.replace("RRRR", "")
            run_dql = rungql.run_query(self.query, self.variables)

        return [run_dql, tree]
