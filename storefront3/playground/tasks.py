from time import sleep 

###########################################################################
# Approach 1 : Using celery object from storefront
# - this couples playground with storefront
###########################################################################

# from storefront.celery import celery

# @celery.task
# def notify_customers(message):
#     print('Sending 10k emails ...')
#     print(message)
#     sleep(10)
#     print('Emails were successfully sent!')

###########################################################################
# Approach 2 : Using celery object from storefront
###########################################################################

from celery import shared_task

@shared_task
def notify_customers(message):
    print('Sending 10k emails ...')
    print(message)
    sleep(10)
    print('Emails were successfully sent!')

###########################################################################    
    
