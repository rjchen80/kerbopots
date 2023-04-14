#!/bin/bash
curl -H 'Connection: keep-alive' -H 'Cache-Control: max-age=0' -H "$1" $2 > $3
