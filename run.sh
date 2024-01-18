#!/bin/bash

/usr/local/bin/opa run -s rego/example.rego -l debug &

python /usr/src/app/app.py

