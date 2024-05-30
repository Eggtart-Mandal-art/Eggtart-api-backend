#!/bin/bash
PID=$(ps aux | grep 'uvicorn main:app --host 0.0.0.0 --port 8000' | grep -v grep | awk '{print $2}')
if [ -z "$PID" ]
then
  echo "No process found"
else
  kill -9 $PID
  echo "Killed process $PID"
fi