virtualenv --python=python3 venv
source venv/bin/activate
pip install -e .
mkdir timg/static/data/
mkdir logs/
touch logs/access.log
touch logs/error.log