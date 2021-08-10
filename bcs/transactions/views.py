import json
from django.http.response import HttpResponse, HttpResponseRedirect
from django.views.generic import TemplateView
from django.shortcuts import render

from .models import Transaction
from .services import RequestError, NetworkService, send_raw_transaction
from .exceptions import RequestError, InsufficientFunds


class TransactionsView(TemplateView):
    template_name = 'transactions.html'

    @property
    def context(self):
        query = Transaction.objects.all()
        return {'transactions': query}

    def get(self, request):
        return render(request,
                      f'transactions/{self.template_name}',
                      context=self.context)

    def create_tx(self):
        tx = NetworkService.create_signed_tx_for_new_address(coins=1)
        tx_hex = tx.as_hex()
        return send_raw_transaction([tx_hex])

    def post(self, request):
        try:
            result = self.create_tx()
            Transaction(id=result).save()
            message = 'Transaction has been sent successfully.'
        except RequestError as e:
            message = str(e)
        except InsufficientFunds:
            message = 'Not enough coins to make Transaction.'
        
        context = self.context
        context['message'] = message
        return HttpResponseRedirect('/')


class TransactionView(TemplateView):
    template_name = 'transaction.html'

    def get(self, request, tx_id):
        try:
            tx = Transaction.objects.get(id=tx_id)
            return render(request,
                          f'transactions/{self.template_name}',
                          context={'tx': tx})
        except Transaction.DoesNotExist:
            return render(request,
                          f'transactions/404.html',
                          context={"id": tx_id})
