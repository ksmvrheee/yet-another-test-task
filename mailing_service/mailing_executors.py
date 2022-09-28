from datetime import datetime
from django.db.models import Q
import requests

from .scheduling import scheduler
from .models import Message, Customer, Mailing
from .secret import TOKEN


def start_mailing(mailing):
    print('Started mailing')

    token = TOKEN
    url = 'https://probe.fbrq.cloud/v1/send/'
    headers = {'Authorization': f'Bearer {token}'}

    customers_list = list(Customer.objects.filter(
        Q(operator_code=mailing.operator_code) & Q(tag=mailing.customer_tag)
    ))

    k = len(customers_list)

    while datetime.now().timestamp() < mailing.finish_datetime.timestamp() and k:
        i = k - 1

        current_msg = Message.objects.create(
            creating_datetime=datetime.now(),
            status=False,
            corresponding_mailing=mailing,
            corresponding_customer=customers_list[i]
        )
        current_msg.save()

        current_msg_num = current_msg.pk
        url += str(current_msg_num)

        data_d = {
            'id': current_msg_num,
            'phone': int(customers_list[i].personal_number),
            'text': mailing.text,
        }

        try:
            response = requests.post(
                url=url,
                headers=headers,
                json=data_d,
            )
        except (requests.RequestException, requests.ConnectionError) as e:
            print(e)
        else:
            current_msg.status = True
            current_msg.save()
            print('Message saved')

        k -= 1


def delete_mailing(pk):
    m = Mailing.objects.filter(pk=pk)

    if not m:
        return {'error': 'Can not found Mailing with such id!'}
    elif m[0].launch_datetime.timestamp() < datetime.now().timestamp() < m[0].finish_datetime.timestamp():
        try:
            scheduler.remove_job(f'mailing_{pk}')
        except:
            m[0].delete()
    m[0].delete()
    return {'message': 'Mailing was successfully deleted.'}

