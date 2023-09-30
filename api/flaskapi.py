from flask import request, url_for
from flask_api import FlaskAPI, status, exceptions
import json

app = FlaskAPI(__name__)
f=open('myfile.json')
data=json.load(f)


def data_repr(key):
    return {
        'url': request.host_url.rstrip('/') + url_for('field', key=key),
        'text': data[key]
    }

@app.route("/", methods=['GET'])
def data_list():
    """
    List or create notes.
    """
    # request.method == 'GET'
    return [data_repr(idx) for idx in sorted(data.keys())]

@app.route("/<int:key>/", methods=['GET', 'PUT', 'DELETE'])
def data_detail(key):
    """
    Retrieve, update or delete note instances.
    """
    if request.method == 'PUT':
        note = str(request.data.get('text', ''))
        data[key] = note
        return data_repr(key)

    elif request.method == 'DELETE':
        data.pop(key, None)
        return '', status.HTTP_204_NO_CONTENT

    # request.method == 'GET'
    if key not in data:
        raise exceptions.NotFound()
    return data_repr(key)

if __name__ == "__main__":
    app.run(debug=True)