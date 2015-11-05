from flask import Flask, render_template
import assets
import logging
import json

LOG_FORMAT = "%(asctime)-15s\t%(levelname)s\t%(name)s\t%(message)s"

def get_logger(name):
    logger = logging.getLogger(name)
    logger.propagate = False
    logger.setLevel(level=logging.DEBUG)
    logger.addHandler(logging.StreamHandler())
    for handler in logger.handlers:
        handler.setFormatter(logging.Formatter(LOG_FORMAT))
    return logger

logger = get_logger("web")

class Application:

    def __init__(self):
        self._flask = Flask(__name__)
        self._flask.config.from_object("config")
        self.config = self._flask.config
        assets.init(self._flask)

        # Add rules.
        self._add_rule("/", "main", methods=["GET"])

    def _add_rule(self, rule, endpoint, methods):
        self._flask.add_url_rule(
            rule,
            endpoint,
            self._process_exception(
                Application.__dict__[endpoint]
            ),
            methods=methods)

    def _process_exception(self, func):
        def decorator(*args, **kwargs):
            try:
                return func(self, *args, **kwargs)
            except Exception as error:
                logger.exception("Unknown error:")
                return json.dumps({"code": 1, "message": "Unknown error: " + str(error)}), 502

        return decorator

    def main(self):
        return render_template("main.html")

    def run(self, *args, **kwargs):
        self._flask.run(*args, **kwargs)

    def get_wsgi_app(self):
        return self._flask

if __name__=="__main__":
    app = Application()
    app.run(host='127.0.0.1', port=8715, debug=True, use_reloader=False)
else:
    app = Application().get_wsgi_app()
