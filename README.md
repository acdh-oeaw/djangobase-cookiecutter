# djangobase-cookiecutter

# DSE-Static-Cookiecutter

[Cookiecutter](https://github.com/cookiecutter/cookiecutter) template djangobaseproject-based django-project

## what is this for

The current repo should ease the process of setting up a djangobaseproject-based django-project

## Quickstart
* Install the latest Cookiecutter if you haven't installed it yet (this requires Cookiecutter 1.7.0 or higher) by running `pip install -U cookiecutter`
* To generate a new djangobaseproject-based django-project project run `cookiecutter gh:acdh-oeaw/djangobase-cookiecutter` and answer the following questions, see below:

```json
{
    "directory_name": "my-new-project",
    "project_title": "My New Project",
    "project_abbr": "mnp",
} 
```
* change into the new created repo, by default `$ my-new-project`
* create a virtual env
* install requierements `pip install -r requirements.txt`
* *optional* add/modfiy environment-variables in `env.default`, rename it into e.g. `env.secret`
* *optional* change `set_env_varibales.sh` so it uses your actual env-file

* run `python manage.py migrate`
* start developing
