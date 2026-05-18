# djangobase-cookiecutter

[Cookiecutter](https://github.com/cookiecutter/cookiecutter) template djangobaseproject-based django-project

## what is this for

The current repo should ease the process of setting up a djangobaseproject-based django-project

## Quickstart

> [!NOTE]
> Make sure you have [uv](https://docs.astral.sh/uv/) installed!

* To generate a new djangobaseproject-based django-project project run `uvx cookiecutter gh:acdh-oeaw/djangobase-cookiecutter` and answer the following questions, see below:

```json
{
    "directory_name": "my-new-project",
    "project_title": "My New Project",
    "project_abbr": "mnp",
    "github": "https://github.com/acdh-oeaw/djangobaseproject",
    "redmine_id": "18716",
}
```

* change into the new created repo, by default `$ my-new-project`
* *optional* add/modfiy environment-variables in `env.default`, rename it into e.g. `env.secret`
* *optional* change `set_env_varibales.sh` so it uses your actual env-file

* run `uv run python manage.py migrate`
* start developing
