import webapp2
import os
import jinja2
import cgi

template_dir = os.path.join(os.path.dirname('__file__'), 'templates')
jinja2_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=True)

class Handler(webapp2.RequestHandler):
    def write(self, *a, **kwa):
        self.response.write(*a, **kwa)
    def render_str(self, template, **kwa):
        t = jinja2_env.get_template(template)
        return t.render(kwa)
    def render(self, template, **kwa):
        self.write(self.render_str(template, **kwa))

class MainPage(Handler):
    def get(self):
        items = self.request.get_all("food")
        # print("items: %s" % items)
        # for i, item in enumerate(items):
        #     items[i] = cgi.escape(items[i])
        self.render("form.html", items=items)

class FizzBuzzPage(Handler):
    def get(self):
        n = self.request.get('n', 0)
        n = n and int(n)
        self.render('fizzbuzz.html', n=n)

class Rot13Handler(Handler):
    def rot13(self, str):
        print('str: %s' % str)
        res = ''
        for char in str:
            asc_n = ord(char)
            if ord('z') >= asc_n >= ord('a'):
                if asc_n + 13 > 122:
                    res += unichr(96 + (asc_n + 13) % 122)
                else:
                    res += unichr(asc_n + 13)
            elif ord('Z') >= asc_n >= ord('A'):
                if asc_n + 13 > 90:
                    res += unichr(64 + (asc_n + 13) % 90)
                else:
                    res += unichr(asc_n + 13)
            else:
                res += char
        return res
    def get(self):
        self.render('rot13.html')
    def post(self):
        print(self.request)
        text = self.request.POST.get('text')
        encoded = self.rot13(text)
        self.render('rot13.html', text = encoded)

app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/fizzbuzz', FizzBuzzPage),
    ('/rot13', Rot13Handler)
], debug=True)
