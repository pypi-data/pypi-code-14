
EMAIL_BACKEND = 'leonardo_celery_emails.backends.FailSilentlyEmailBackend'

CELERY_EMAIL_TASK_CONFIG = {
    'name': 'djcelery_email_send',
    'ignore_result': False,
}
