export secret=$(python create-token.py)
export app_id=${RANDOM}${RANDOM}
echo Running server with app_id $app_id and secret $secret

python server.py
