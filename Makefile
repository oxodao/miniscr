.PHONY: lint lint-fix deb

lint:
	uv run ruff check .

lint-fix:
	uv run ruff check . --fix

deb:
	dpkg-buildpackage -us -uc -b
