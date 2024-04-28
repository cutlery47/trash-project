import os
import sys

# Builtin WSGI server
# TODO: change this to gunicorn when pushing to prod
def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'user_service.wsgi.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Django is required to run manage.py ..."
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
