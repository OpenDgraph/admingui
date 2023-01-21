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

import pyperclip
import arguments as _args
import json


def separators_constructor(data, response=None, JSON=False):
    _response = ""

    if JSON is True:
        endTime = data['extensions']['tracing']['endTime']
        duration = data['extensions']['tracing']['duration']
        duration = duration / 1000000
        _data = json.dumps(data, indent=4, sort_keys=True)
        _response = f"------------------ Response {list(data['data'].keys())} ------------------\n"
        _response += f"{_data}\n"
        _response += f'\nDuration: {duration} ms\nEndTime: {endTime}\n'
        _response += "------------------ End of Response ------------------\n\n"
    elif "errors" in str(data):
        _response = "------------------      Error      ------------------\n"
        _response += f"{data['errors'][0]['message']}\n"
        _response += "------------------ End of Error ------------------\n"
    elif "exceeded" in str(data):
        _response = "------------------      Error      ------------------\n"
        _response += f"{data}\n"
        _response += "------------------ End of Error ------------------\n"
        _response += "This usually means that the Cluster is not locally accessible.\n"
    else:
        endTime = data[0]['extensions']['tracing']['endTime']
        duration = data[0]['extensions']['tracing']['duration']
        duration = duration / 1000000
        _response = f"------------------ Response {list(data[0]['data'].keys())} ------------------\n"
        # _response += f"{data}\n"
        _response += f'{response}\nDuration: {duration} ms\nEndTime: {endTime}\n'
        _response += "------------------ End of Response ------------------\n\n"
    if "Unauthenticated" in str(data) or "PermissionDenied" in str(data):
        _response += "Try to login in the ACL tab and Login sub tab\n"
    return _response


def copy_to_clipboard():
    if _args.arguments.token is not None:
        pyperclip.copy(_args.arguments.token)
