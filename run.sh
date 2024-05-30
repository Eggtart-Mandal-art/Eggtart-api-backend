#!/bin/bash
export PATH="$HOME/.local/bin:$PATH"
export LD_LIBRARY_PATH="/opt/instantclient_19_22"
poetry shell
cd src
nohup uvicorn main:app --host 0.0.0.0 --port 8000 >> output.log 2>&1 &
