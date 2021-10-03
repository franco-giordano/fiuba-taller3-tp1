from flask import render_template

def get_app(request):
    """Responds to any HTTP request.
    Args:
        request (flask.Request): HTTP request object.
    Returns:
        The response text or any set of values that can be turned into a
        Response object using
        `make_response <http://flask.pocoo.org/docs/1.0/api/#flask.Flask.make_response>`.
    """
    if request.args and 'page' in request.args:
        req_file = request.args.get('page')
        # return redirect(f"https://storage.googleapis.com/fgiordano-static/pages/{req_file}.html")
        return render_template(f'{req_file}.html')
    else:
        return f'Provide type with ?page=...'
