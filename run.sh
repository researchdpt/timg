source venv/bin/activate
source config
echo "=== Configuration ==="
echo "HOST:" $HOST
echo "PORT:" $PORT

echo ""

echo "=== Starting Server ==="
flask run --host=$HOST --port=$PORT
