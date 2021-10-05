from flask import render_template

def get_app(request):
    # TODO: 
    # - handle req_file exception
    # - make RESTful?
    if request.args and 'page' in request.args:
        req_file = request.args.get('page')
        return render_template(f'{req_file}.html')
    else:
        return f'Provide type with ?page=...'
