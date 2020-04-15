#!/bin/bash
waitress-serve --call 'flaskr:create_app'
