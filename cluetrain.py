#!/usr/bin/env python
#
# Copyright 2007 Beat Bolli <me+appspot@drbeat.li>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os, random
import datetime
import wsgiref.handlers
import logging

from google.appengine.ext import webapp
from google.appengine.ext.webapp import template

from theses import theses


root_path = os.path.dirname(__file__)

class TemplatePage(webapp.RequestHandler):

    def render(self, template_file, context={}):
        self.response.out.write(template.render(
            os.path.join(root_path, template_file), context
        ))

class RandomPage(webapp.RequestHandler):
    def get(self):
        n = random.randint(1, len(theses['en']))
        self.redirect('/%d' % n)

class ThesisPage(TemplatePage):
    default_lang = 'en'

    def get(self, n):
        available = theses.keys()
        for lang in self.language():
            if lang in available:
                break
        else:
            lang = self.default_lang
        th = theses[lang]
        n = int(n)
        if 1 <= n <= len(th):
            context = {'n': n, 'thesis': th[n - 1]}
            if n > 1:
                context['first'] = 1
                context['prev'] = n - 1
            if n < len(th):
                context['next'] = n + 1
                context['last'] = len(th)
        else:
            context = {'n': 404, 'thesis': 'Not found', 'first': 1, 'last': len(th)}
        self.render('index.html', context)

    def language(self):
        lang = self.request.headers.get('accept-language')
        if not lang:
            return []
        accepted = []
        for lq in [l.split(';') for l in lang.split(',')]:
            attrs = dict(l.split('=', 1) for l in lq[1:])
            try:
                q = float(attrs.get('q', '1.0'))
            except ValueError:
                q = 0
            accepted.append((q, lq[0][:2]))
        accepted.sort(reverse=True)
        return [a[1] for a in accepted]

class AboutPage(TemplatePage):
    def get(self):
        self.render('about.html')


application = webapp.WSGIApplication([
    ('/', RandomPage),
    ('/(\d+)', ThesisPage),
    ('/about', AboutPage),
], debug=False)


def main():
    wsgiref.handlers.CGIHandler().run(application)

if __name__ == '__main__':
    main()
