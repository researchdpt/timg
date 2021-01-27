source venv/bin/activate
source config

echo "=== Starting Server ==="
uwsgi --socket $HOST:7000 --module timg --master --enable-threads --workers 8 --processes 8 --threads 4 --callab app -H venv
