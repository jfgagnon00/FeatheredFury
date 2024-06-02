source .configs/variables.sh

$(PYTHON_INTERPRETER) -m pip install -q virtualenv

@echo "source $(CI_DIR)/activate_environment.sh $(PYTHON_INTERPRETER) $(PROJECT_NAME)" > activate.sh
@chmod 755 activate.sh
@echo \"source activate.sh\" pour activer environment python
