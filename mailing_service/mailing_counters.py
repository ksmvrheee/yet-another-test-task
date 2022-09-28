from django.db.models import Q

from .models import Mailing, Message


def get_mailing_general_statistic():
    queryset = Mailing.objects.all()
    data = {}

    for el in queryset:
        data[el] = {}
        data[el]['Sent messages'] = Message.objects.filter(Q(corresponding_mailing=el) & Q(status=True)).count()
        data[el]['Unsent messages'] = Message.objects.filter(Q(corresponding_mailing=el) & Q(status=False)).count()

    if not data:
        return {'error': 'Have not found any mailings!'}

    return data


def get_mailing_special_statistic(mailing_id):
    mailing_instance = Mailing.objects.filter(pk=mailing_id)

    if not mailing_instance:
        return {'error': 'Can not found Mailing with such id!'}

    data = {
        'Sent messages': Message.objects.get(Q(corresponding_mailing=mailing_instance[0]) & Q(status=True)).count(),
        'Unsent messages': Message.objects.get(Q(corresponding_mailing=mailing_instance[0]) & Q(status=False)).count(),
    }

    return data
