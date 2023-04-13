"""
Для подключения admin нужно создать этот файл, добавить путь
/admin в urls.py и приложение в settings.py (INSTALLED_APPS).
После этого необходимо выполнить команду, чтобы создать учетную
запись администратора:

python manage.py createsuperuser

Перед этой командой может понадобиться выполнить команду для
синхронизации БД:

python manage.py migrate --run-syncdb
"""
from django.contrib import admin
from proj_maths.models import Doctors, Patients

admin.site.register(Doctors)  # Регистрируем таблицы БД для отображения в admin
admin.site.register(Patients)
