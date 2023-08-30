import shutil


if "{{ cookiecutter.appcreator }}" == "no":
    print("removing appcreator code")
    shutil.rmtree("./appcreator")

if "{{ cookiecutter.database }}" == "postgres":
    shutil.copyfile("./default.env", "./secret.env")