import pyperclip
import arguments as _args


def separators_constructor(data, response=None):
    _response = ""
    if "errors" in str(data):
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
        _response += "Try to login in the login tab\n"
    return _response


def copy_to_clipboard():
    if _args.arguments.token is not None:
        pyperclip.copy(_args.arguments.token)
