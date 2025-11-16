#!/bin/bash
# run.sh

# Default to first script if none is provided (use repo-relative path)
# When the container's CWD is `/app`, scripts live in `script_to_gen_horoscope_and_stor/`.
SCRIPT=${1:-script_to_gen_horoscope_and_stor/query_script_with_flask.py}

echo "Running $SCRIPT ..."
python "$SCRIPT"
