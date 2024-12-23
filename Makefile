files_to_fmt ?= src settings.py migrate.py
files_to_check ?= src settings.py migrate.py

## Format all
fmt: rm_imports isort black docformatter add-trailing-comma


## Check code quality
chk: flake8 black_check docformatter_check


## Remove unused imports
rm_imports:
	autoflake -ir --remove-unused-variables \
		--ignore-init-module-imports \
		--remove-all-unused-imports \
		${files_to_fmt}


## Sort imports
isort:
	isort ${files_to_fmt}


## Format code
black:
	# black does not work recursively (may be it's a bug?),
	# so we use 'find'
	find ${files_to_fmt} -name "*.py" -exec black {} + \


## Check code formatting
black_check:
	black ${files_to_fmt} --check


## Format docstring
docformatter:
	docformatter -ir ${files_to_fmt}


## Check docstring formatting
docformatter_check:
	docformatter -cr ${files_to_check}


## Add trailing comma
add-trailing-comma:
	find ${files_to_fmt} -name "*.py" -exec add-trailing-comma {} + \


## Check pep8
flake8:
	flake8 ${files_to_check}


## Check typing
mypy:
	mypy ${files_to_check}


## Check if all dependencies are secure and do not have any known vulnerabilities
safety:
	safety check --bare --full-report


## Check code security
bandit:
	bandit -r ${files_to_check} -x tests -s B608
