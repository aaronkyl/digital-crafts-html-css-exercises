import tornado.ioloop
import tornado.web
import os

from jinja2 import Environment, PackageLoader, select_autoescape
  
ENV = Environment(
    loader=PackageLoader('myapp', 'templates'),
    autoescape=select_autoescape(['html', 'xml']))
    
class TemplateHandler(tornado.web.RequestHandler):
    def render_template (self, tpl, context):
        template = ENV.get_template(tpl)
        self.write(template.render(**context))

class MainHandler(TemplateHandler):
    def get(self):
        self.render_template("home.html", {})

class CtoFHandler(TemplateHandler):
    def get(self):
        celsius = self.get_query_argument("celsius", None)
        if celsius:
            fahrenheit = float(celsius) * 1.8 + 32
            self.render_template("c-to-f.html", {"celsius": celsius, "fahrenheit": fahrenheit})
        else:
            self.render_template("c-to-f.html", {})

def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/c-to-f", CtoFHandler),
        (
            r"/static/(.*)",
            tornado.web.StaticFileHandler,
            {'path': 'static'}
        ),
        ], autoreload=True)

if __name__ == "__main__":
    tornado.log.enable_pretty_logging()

    app = make_app()
    PORT = int(os.environ.get('PORT', '8080'))
    app.listen(PORT)
    tornado.ioloop.IOLoop.current().start()