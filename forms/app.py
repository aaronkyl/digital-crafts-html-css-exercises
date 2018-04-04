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

class WorkOrSleepInHandler(TemplateHandler):
    def get(self):
        days_of_week = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
        day = self.get_query_argument("day", None)
        if day:
            day = int(day)
            if day > 0 and day < 6:
                result = "work"
            else:
                result = "sleep in"
            day = days_of_week[day]
            self.render_template("work-or-sleep-in.html", {"day": day, "result": result})
        else:
            self.render_template("work-or-sleep-in.html", {})

def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/c-to-f", CtoFHandler),
        (r"/work-or-sleep-in", WorkOrSleepInHandler),
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