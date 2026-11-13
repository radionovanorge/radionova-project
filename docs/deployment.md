# Azure deployment

`main_radionova.yml` deploys pushes to `main` to production. Other branches
are not deployed automatically. Do not use workflow_dispatch for a test app:
it still targets production.

The build job runs the deployment tests and creates a source ZIP using:

```sh
python -m unittest discover -s tests -v
python scripts/build_deploy_package.py release.zip
```

Only tracked application files are included. Local environments, node_modules,
credentials, CI configuration and nested ZIPs are excluded. Stage new application
files before building locally. The deploy job uses `package: release.zip`, not
its working directory. Python requirements are installed in that job for database
migrations; Azure/Oryx creates the runtime environment. Oryx is the sole owner of
collectstatic. Keep Azure build automation enabled and collectstatic enabled.

WSGI writes `STARTUP django_loading`, then `django_ready` with elapsed time, or
`django_failed`. Startup taking over 30 seconds emits repeating faulthandler
stacks until initialization ends. These stacks contain filenames and frames,
without local variables or environment dumps. This is diagnostic logging, not a
health check or an increase to the startup timeout.

## Validation before production

Use the isolated F1 app `radionova-diagnostic-20261111`, never the production plan.
Its Python 3.11/SQLite settings and startup wrapper are test-only overlays and
must not be merged into production. Production uses Python 3.10, PostgreSQL,
Azure Storage and VNet; passing the isolated test does not verify those services.

Check successful Oryx build/collectstatic, the new STARTUP messages, HTTP status
and Wagtail content at `/admin/login/`. After production deployment, check the
actual website content and admin login as well as Actions and container startup
logs. A successful Actions job alone does not verify runtime health.

If runtime fails, inspect startup stacks before changing settings or scaling.
Reverting the deployment changes restores the previous workflow and WSGI entry
point; it does not undo database migrations.
