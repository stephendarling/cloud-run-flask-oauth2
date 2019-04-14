import os

import flask
from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello_world():
    target = os.environ.get('TARGET', 'World')
    result_message = {
        'message': f'Hello {target} from authenticated Cloud Run!'
    }
    return flask.jsonify(result_message)

if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0',port=int(os.environ.get('PORT', 8080)))