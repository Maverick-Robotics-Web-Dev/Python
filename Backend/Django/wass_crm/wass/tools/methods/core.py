from django.core.exceptions import ImproperlyConfigured
import json


def get_env_file(secret_name):
    try:
        with open("core/core_env_v.json") as f:
            secret_file = json.loads(f.read())
        return secret_file[secret_name]
    except:
        msg = f'La Variable {secret_name} no existe'
        raise ImproperlyConfigured(msg)
