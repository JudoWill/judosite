#!/bin/bash
virtualenv judosite --no-site-packages
source ./ve/bin/activate
pip install -e git://github.com/cmheisel/nose-xcover.git#egg=nosexcover
pip install -q -E ./judosite -r requirements.pip

python manage.py test --with-coverage --cover-package=DistAnnot --with-xunit --with-xcoverage