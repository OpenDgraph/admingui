import argparse

parser = argparse.ArgumentParser()

parser.add_argument("-c", "--hostname", help="Cluster hostname")
parser.add_argument("-u", "--username", help="ADmin user name")
parser.add_argument("-p", "--password", help="Password")
parser.add_argument("-t", "--token", help="JWT Token")
parser.add_argument("-r", "--refreshJWT", help="Refresh Token JWT")
parser.add_argument("-j", "--JSON", help="Response as JSON")

global arguments

arguments = parser.parse_args()
