source configs/variables.sh

# valider si interpreteur python est present
${CI_DIR}/test_python_interpreter.sh ${PYTHON_INTERPRETER}
if [ $? -ne 0 ]; then
    echo "$PYTHON_INTERPRETER n'est pas accessible"
	exit 1
fi

# installer virtualenv
$PYTHON_INTERPRETER -m pip install -q virtualenv

# generer script pour activation environment virtuel
echo "source ${CI_DIR}/activate_environment.sh ${PYTHON_INTERPRETER} ${PROJECT_NAME} \$*" > activate.sh
chmod 755 activate.sh

# indication a l'utilisateur
echo \"source activate.sh\" pour activer environment python
