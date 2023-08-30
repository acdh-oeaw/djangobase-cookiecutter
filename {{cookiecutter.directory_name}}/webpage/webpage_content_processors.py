from django.conf import settings

def my_app_name(request):
    return {"PROJECT_NAME": settings.PROJECT_NAME}


def installed_apps(request):
    return {"APPS": settings.INSTALLED_APPS}


def get_db_name(request):
    try:
        db_name = settings.DATABASES["default"]["NAME"]
        return {"DB_NAME": db_name}
    except (AttributeError, KeyError):
        return {}
