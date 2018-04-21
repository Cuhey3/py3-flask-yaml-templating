from flask import Flask, render_template
from custom_filters import add_all_filters
from util.app_util import get_nested_value

app = Flask(__name__)
add_all_filters(app.jinja_env.filters)


@app.route('/<username>')
def controller(username):
    return render_template('index.html', title='flask test', username=username)


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8080)
