from flask import Flask

class Application:

    def __init__(self):
        self._flask = Flask(__name__)
        self._flask.config.from_object("config")
        self.config = self._flask.config

    def run(self, *args, **kwargs):
        self._flask.run(*args, **kwargs)

    def get_wsgi_app(self):
        return self._flask

if __name__=="__main__":
    app = Application()
    app.run(host='127.0.0.1', port=8715, debug=True, use_reloader=False)
else:
    app = Application().get_wsgi_app()
