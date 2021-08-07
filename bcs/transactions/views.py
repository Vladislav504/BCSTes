from django.http.response import HttpResponse, HttpResponseRedirect
from django.views.generic import TemplateView
from django.shortcuts import render
import requests

from .models import Transaction
from .services import get_new_address
from base.services import get_base_network


class TransactionsView(TemplateView):
    template_name = 'transactions.html'

    def get(self, request):
        query = Transaction.objects.all()
        context = {'transactions': query}
        return render(request,
                      f'transactions/{self.template_name}',
                      context=context)

    def post(self, request):
        new_address = get_new_address()
        network = get_base_network()
        return HttpResponseRedirect('/')


class TransactionView(TemplateView):
    template_name = 'transaction.html'

    def get(self, request, tx_id):
        try:
            tx = Transaction.objects.get(id=tx_id)
            print(tx)
            return render(request,
                          f'transactions/{self.template_name}',
                          context={'tx': tx})
        except Transaction.DoesNotExist:
            return render(
                request,
                f'transactions/404.html',
                context={"id": tx_id}
            )
