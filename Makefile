run:
	cd demo && python run.py

test:
	ruff .
	cd tests && pytest -v

test-v:
	cd tests && pytest -vv