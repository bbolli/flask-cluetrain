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

from google.appengine.ext import webapp
from google.appengine.ext.webapp import template

from theses import theses


class RandomPage(webapp.RequestHandler):
    def get(self):
	n = random.randint(1, len(theses))
	self.redirect('/%d' % n)

class ThesisPage(webapp.RequestHandler):
    def get(self, n):
	n = int(n)
	context = {'n': n}
	if 1 <= n <= len(theses):
	    context['thesis'] = theses[n - 1]
	    if n > 1:
		context['prev'] = n - 1
	    if n < len(theses):
		context['next'] = n + 1
	else:
	    context = {'n': 404, 'thesis': 'Not found', 'prev': 1, 'next': len(theses)}
	path = os.path.join(os.path.dirname(__file__), 'index.html')
	self.response.out.write(template.render(path, context))


application = webapp.WSGIApplication([
    ('/', RandomPage),
    ('/(\d+)', ThesisPage),
], debug=True)


def main():
    wsgiref.handlers.CGIHandler().run(application)

if __name__ == '__main__':
    main()
