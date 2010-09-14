#!/bin/bash
virtualenv judosite --no-site-packages
source ./ve/bin/activate
pip install -e git://github.com/cmheisel/nose-xcover.git#egg=nosexcover
pip install -e http://github.com/glamkit/glamkit-eventtools.git
pip install -q -E ./judosite -r requirements.pip

python manage.py test --with-coverage --with-xunit --with-xcoverage