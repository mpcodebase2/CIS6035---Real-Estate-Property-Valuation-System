from flask import Flask, render_template, request, jsonify

list_app = Flask(__name__)
list_app.config.from_object('config.Config')

@list_app.route('/add_bar', methods=['POST'])
def add_bar():
    return jsonify(success=True)

if __name__ == '__main__':
    list_app.run(debug=True)
