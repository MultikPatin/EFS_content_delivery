#!/bin/bash

export PYTHONPATH=$SRC_PATH

python3 tests/functional/utils/wait_for_es.py

python3 tests/functional/utils/wait_for_redis.py

pytest tests/functional/src
