test:
	ruff .
	cd tests && pytest -v

test-v:
	cd tests && pytest -vv

pip-update:
	python -m pip install --upgrade pip

pip-editable:
	pip install -e . --config-settings editable_mode=compat