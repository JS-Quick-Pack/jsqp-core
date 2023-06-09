demo:
	cd demo && python demo.py

test:
	ruff .
	cd tests && pytest -v

test-v:
	cd tests && pytest -vv