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

import datetime
import os
import random

from flask import (
    Flask,
    redirect,
    render_template,
    request,
    url_for,
)

from theses import theses

app = Flask(__name__)


@app.route('/')
def index():
    n = random.randint(1, len(theses['en']))
    return redirect(url_for('thesis', n=n))


@app.route('/<int:n>')
def thesis(n):
    lang = request.accept_languages.best_match(theses.keys(), 'en')
    th = theses[lang]
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
    return render_template('index.html', **context)


@app.route('/about')
def about():
    return render_template('about.html')


if __name__ == '__main__':
    app.run()
