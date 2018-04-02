from flask import Flask, render_template
app = Flask(__name__)


@app.route('/<username>')
def controller(username):
    return render_template('index.html', title='flask test', username=username)


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8080)
