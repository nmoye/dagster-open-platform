uv_install:
	pip install uv

test_install: uv_install
	uv pip install -e ".[tests]"

dev_install: uv_install
	uv pip install -e ".[dev]"
	cd dagster_open_platform_dbt && dbt deps && cd ..

test: test_install
	pytest dagster_open_platform_tests

manifest:
	cd dagster_open_platform_dbt && dbt parse && cd ..

dev:
	make manifest
	dagster dev

lint:
	sqlfluff lint ./dagster_open_platform_dbt/models --disable-progress-bar --processes 4

fix:
	sqlfluff fix ./dagster_open_platform_dbt/models --disable-progress-bar --processes 4

install_ruff:
	$(MAKE) -C ../.. install_ruff

ruff:
	$(MAKE) -C ../.. ruff