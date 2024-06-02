#!/bin/bash

# script verifie si python est accessible
PYTHON_INTERPRETER=$1

ver=`$PYTHON_INTERPRETER -c "import sys; print(sys.version_info.major)" > /dev/null 2>&1`
if [ -z "$ver" ]; then
	exit 1
fi
exit 0