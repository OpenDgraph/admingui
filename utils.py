def separators_constructor(data, response=None):
    print("separators_constructor data", data)
    _response = ""
    if "errors" in data:
        _response = "------------------      Error      ------------------\n"
        _response += f"{data['errors'][0]['message']}\n"
        _response += "------------------ End of Error ------------------\n"
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
