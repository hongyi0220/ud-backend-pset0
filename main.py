import webapp2
import os
import jinja2
import cgi
import re
import urllib

template_dir = os.path.join(os.path.dirname('__file__'), 'templates')
jinja2_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=True)

class Handler(webapp2.RequestHandler):
    def write(self, *a, **kwa):
        self.response.write(*a, **kwa)

    # def redirect(self, *a, **kwa):
    #     self.redirect()

    def render_str(self, template, **kwa):
        t = jinja2_env.get_template(template)
        return t.render(kwa)

    def render(self, template, **kwa):
        self.write(self.render_str(template, **kwa))

    # def render_redirect(self, template, **kwa):
    #     self.render_str(

class MainPage(Handler):
    def get(self):
        items = self.request.get_all("food")
        # print("items: %s" % items)
        # for i, item in enumerate(items):
        #     items[i] = cgi.escape(items[i])
        self.render("form.html", items=items)

class FizzBuzzHandler(Handler):
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
        self.render('rot13.html', text=encoded)

class SignupHandler(Handler):
    def get(self):
        self.render('signup.html')

    def post(self):
        def valid_username(username):
            USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
            return USER_RE.match(username)

        def valid_password(password):
            PASSWORD_RE = re.compile(r"^.{3,20}$")
            return PASSWORD_RE.match(password)

        def valid_email(email):
            EMAIL_RE = re.compile(r"^[\S]+@[\S]+.[\S]+$")
            return EMAIL_RE.match(email)

        username = self.request.POST.get('username')
        password = self.request.POST.get('password')
        verify = self.request.POST.get('verify')
        email = self.request.POST.get('email')
        print('username:', username)
        print('password:', password)
        print('email', email)

        invalid_username = '' if valid_username(username) else 'Invalid username'
        invalid_password = '' if valid_password(password) else 'Invalid password'
        invalid_verify = '' if valid_password(password) and \
                               password == verify else 'Passwords don\'t match'
        invalid_email = '' if not email or valid_email(email) else 'Invalid email address'

        if valid_username(username) and valid_password(password) and password == verify and email:
            if valid_email(email):
                return self.redirect(
                    '/welcome?' + urllib.urlencode({'username': username}))
            else:
                self.render('signup.html', invalid_email=invalid_email, username=username)
        elif valid_username(username) and valid_password(password) and password == verify:
            return self.redirect('/welcome?' + urllib.urlencode({'username': username}))
        else:
            self.render(
                'signup.html',
                invalid_username=invalid_username,
                invalid_password=invalid_password,
                invalid_verify=invalid_verify,
                invalid_email=invalid_email,
                username=username,
                email=email)

class WelcomeHandler(Handler):
    def get(self):
        username = self.request.get('username')
        print(username)
        self.render('welcome.html', username=username)

app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/fizzbuzz', FizzBuzzHandler),
    ('/rot13', Rot13Handler),
    ('/signup', SignupHandler),
    ('/welcome', WelcomeHandler)
], debug=True)
