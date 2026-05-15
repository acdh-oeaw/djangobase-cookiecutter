import shutil

if "{{ cookiecutter.database }}" == "postgres":
    shutil.copyfile("./default.env", "./secret.env")