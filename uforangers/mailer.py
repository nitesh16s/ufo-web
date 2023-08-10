from django.core.checks.messages import Error
from uforangers.settings import EMAIL_HOST_USER
from django.core.mail import send_mail, send_mass_mail
from celery import shared_task


@shared_task
def sendmail(subject, message, to):
    '''
    usage:
    sendmail.delay(
        subject=subject, 
        message=message, 
        to=mail)
    '''
    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=EMAIL_HOST_USER,
            recipient_list=[to]
        )
        return 'Success, Mail sent.'
    except:
        return Error('Email cannot be sent.')