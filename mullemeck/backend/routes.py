from flask import Flask

app = Flask(__name__)


@app.route('/')
def index():
    return '<h1>Hello world!</h1>'


__all__ = ['app']
