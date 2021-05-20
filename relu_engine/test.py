from flask import Flask
import json
app = Flask(__name__)


@app.route('/test', methods=['GET'])
def post_info():
    a = 1
    b = 2
    c = a + b
    return json.dumps(c)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)