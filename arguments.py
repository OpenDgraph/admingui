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
