import os


class GetGQL:
    def __init__(self, file):
        self.file = file

    def read_gql_file(self):
        path = os.path.join(os.getcwd(), 'graphql', self.file + '.gql')
        with open(path, 'r') as f:
            return f.read()
