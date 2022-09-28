from datetime import datetime

from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView

from .scheduling import scheduler
from .mailing_counters import get_mailing_general_statistic, get_mailing_special_statistic
from .mailing_executors import start_mailing, delete_mailing
from .models import Customer, Mailing
from .serializers import CustomerSerializer, MailingSerializer


class CustomerAPIManager(generics.CreateAPIView, generics.RetrieveUpdateDestroyAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer


class MailingAPIManager(generics.CreateAPIView, generics.RetrieveUpdateAPIView):
    queryset = Mailing.objects.all()
    serializer_class = MailingSerializer


class MailingStatistic(APIView):
    def get(self, request, **kwargs):
        if not kwargs.get('pk', False):
            return Response({'General mailings statistic': get_mailing_general_statistic()})
        return Response(
                {f'Statistic of Mailing with number {kwargs["pk"]}': get_mailing_special_statistic(kwargs["pk"])}
        )


class MailingStarterView(APIView):
    def post(self, request, pk):
        mailing_instance = Mailing.objects.filter(pk=pk)

        if not mailing_instance:
            return Response({'error': 'Cannot find such mailing!'})

        if isinstance(mailing_instance[0].launch_datetime, datetime):
            print("TRUE")
        scheduler.add_job(
            start_mailing,
            'date',
            run_date=mailing_instance[0].launch_datetime.replace(tzinfo=None),
            args=[mailing_instance[0], ],
            id=f'mailing_{pk}'
        )
        if datetime.now() >= mailing_instance[0].launch_datetime:
            return Response({'message': 'Mailing has started.'})
        else:
            return Response({'message': f'Mailing will start at {mailing_instance[0].launch_datetime}'})


class MailingDeleterView(APIView):
    def delete(self, request, pk):
        return Response(delete_mailing(pk))
