#!/usr/bin/env python3
#
# Copyright 2007-2021 Beat Bolli <me+python@drbeat.li>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
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

app = Flask(__name__, static_folder=None)


def url_for_thesis(n):
    return url_for('thesis', n=n)


@app.route('/')
def index():
    n = random.randint(1, len(theses['en']))
    return redirect(url_for_thesis(n))


@app.route('/<int:n>')
def thesis(n):
    lang = request.accept_languages.best_match(theses.keys(), 'en')
    th = theses[lang]
    if 1 <= n <= len(th):
        context = {'n': n, 'thesis': th[n]}
        if n > 1:
            context['first'] = url_for_thesis(1)
            context['prev'] = url_for_thesis(n - 1)
        if n < len(th):
            context['next'] = url_for_thesis(n + 1)
            context['last'] = url_for_thesis(len(th))
    else:
        context = {
            'n': 404, 'thesis': th[0],
            'first': url_for_thesis(1), 'last': url_for_thesis(len(th))
        }
    return render_template('index.html', **context)


@app.route('/about')
def about():
    return render_template('about.html')


if __name__ == '__main__':
    app.run()
