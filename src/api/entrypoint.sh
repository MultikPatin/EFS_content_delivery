export PYTHONPATH=$SRC_PATH
rm poetry.lock
rm pyproject.toml
cd "$APP_DIR" || exit
rm Dockerfile
gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind "$API_HOST":"$API_PORT"
