import sys

try:
    from django.conf import settings

    settings.configure(
        DEBUG=True,
        USE_TZ=True,
        DATABASES={
            "default": {
                "ENGINE": "django.db.backends.sqlite3",
            }
        },
        ROOT_URLCONF="djwebhooks.urls",
        INSTALLED_APPS=[
            "django.contrib.auth",
            "django.contrib.contenttypes",
            "django.contrib.sites",
            "djwebhooks",
        ],
        SITE_ID=1,
        NOSE_ARGS=['-s'],
        WEBHOOK_ATTEMPTS=[0, 0, 0],
        WEBHOOK_EVENTS=['test.success', 'test.failure'],
        WEBHOOKS_SENDER="djwebhooks.senders.orm.sender",
        RQ_QUEUES={
            'default': {
                'HOST': 'localhost',
                'PORT': 6379,
                'DB': 0,
            },
            'high': {
                'HOST': 'localhost',
                'PORT': 6379,
                'DB': 0,
            },
            'low': {
                'HOST': 'localhost',
                'PORT': 6379,
                'DB': 0,
            }
        }
    )

    from django_nose import NoseTestSuiteRunner
except ImportError:
    raise ImportError("To fix this error, run: pip install -r requirements-test.txt")


def run_tests(*test_args):
    if not test_args:
        test_args = ['tests']

    # Run tests
    test_runner = NoseTestSuiteRunner(verbosity=1)

    failures = test_runner.run_tests(test_args)

    if failures:
        sys.exit(failures)


if __name__ == '__main__':
    run_tests(*sys.argv[1:])
