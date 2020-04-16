#!/bin/bash
waitress-serve --call --threads=8 'flaskr:create_app'
