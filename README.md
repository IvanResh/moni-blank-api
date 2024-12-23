# moni-blank-api

# Adding a Package
Use the `pip-tools` package manager: `pip install pip-tools`.  
Add the package name to the `requirements` file and run `pip-compile`.

# Migrations

#### Adding a Migration
Run: `yoyo new -m my-new-migration`.

#### Applying Migrations
Run: `python migrate.py`.

#### Rolling Back the Last Migration
Run: `python migrate.py --rollback-one`.

#### Rolling Back All Migrations
Run: `python migrate.py --rollback`.

# Development

To add a new method:
- Create its business logic handler in `src.application.handlers.<folder>.<name>_handler.py`.
- Create its web handler in `src.api.handlers.<folder>.handlers.<name>_handler`.
- Configure dependencies in `api.app._setup_di`.

Before pushing, run `make fmt` and `make chk`.

After creating a web handler:
- Add it to the routes at the bottom of the file.
- If a new group of routes is added, include it in `api.routes`.

# Running the Application

Run: `python -m src.api.app`
