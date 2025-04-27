import os

# Визначаємо, яке середовище використовувати
env = os.environ.get('DJANGO_ENV', 'dev')

if env == 'prod':
    from .prod import *
elif env == 'dev':
    from .dev import *
else:
    from .dev import *
