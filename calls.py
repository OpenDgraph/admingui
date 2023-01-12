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
        for i in range(3):
            tree.pop(0)
        final = list(filter(None, tree))

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
            run_dql = rungql.run_mutation(self.query, self.variables)

        return [run_dql, final]
