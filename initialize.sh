source configs/variables.sh

${CI_DIR}/test_python_interpreter.sh
if [ $? -ne 0 ]; then
    echo "$PYTHON_INTERPRETER n'est pas accessible"
	exit 1
fi

$PYTHON_INTERPRETER -m pip install -q virtualenv

echo "source ${CI_DIR}/activate_environment.sh ${PYTHON_INTERPRETER} ${PROJECT_NAME}" > activate.sh
chmod 755 activate.sh
echo \"source activate.sh\" pour activer environment python
