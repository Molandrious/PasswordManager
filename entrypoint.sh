#!/bin/bash
granian src/main:make_app --factory --interface asgi --loop uvloop --host 0.0.0.0 --port 8000
