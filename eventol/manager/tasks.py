from celery import shared_task
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)


# TODO: remove debug task
@shared_task
def send_welcome_email(user_email):
    '''
    Fake task to Simulating sending an email
    '''
    print(f"Sending welcome email to {user_email}")
    logger.info('Calling mytask with %s', user_email)
    return f"Email sent to {user_email}"
