from flask_assets import Bundle, Environment
import subprocess
import json
from pprint import pprint

environment = None

js_list = []
less_list = []

common_js = None
common_css = None

def process_row(k, v):
    remove_static = lambda path: path.replace("static/","")
    if isinstance(v, list):
        for vn in v:
            process_row(k, vn);
    else:
        if v.find('js') != -1:
            js_list.append(remove_static(v))
        else:
            less_list.append(remove_static(v))

def create_bundle():
    res = subprocess.check_output(['bower', 'list', '-p', '-r', '-j'])
    bower_components = json.loads(res)
    for k, v in bower_components.iteritems():
        process_row(k, v)

    global common_js 
    global common_css

    less_list.append('css/main.css')

    common_css = Bundle(
        *less_list,
        filters='less, cssmin',
        output='public/css/common.css')

    js_list.append('js/main.js')

    common_js = Bundle(
        *js_list,
        filters='closure_js',
        output='public/js/common.js')


def init(app):
    global environment
    create_bundle()
    environment = Environment(app)
    environment.register('common_css', common_css)
    environment.register('common_js', common_js)
    environment.init_app(app)

def main():
    import reporter, logging
    from webassets.script import CommandLineEnvironment

    create_bundle()

    init(reporter.app)

    log = logging.getLogger('webassets')
    log.addHandler(logging.StreamHandler())
    log.setLevel(logging.DEBUG)

    cmdenv = CommandLineEnvironment(environment, log)
    cmdenv.build()

if __name__=="__main__":
    main()
