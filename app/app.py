from flask import Flask, jsonify, request


app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    return jsonify({
        'data': request.json if request.is_json else 'Empty payload',
    })


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
