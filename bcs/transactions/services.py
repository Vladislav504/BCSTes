from pycoin.networks.bitcoinish import Network
from typing import List
from django.conf import settings

from base.services import get_base_network
from .utils import log_error, make_rpc_request, HttpRequester
from .exceptions import InsufficientFunds, RequestError


class NetworkService:
    network: Network = get_base_network()
    coin_mul: int = 1e8
    fee: int = settings.STANDARD_FEE
    wif: str = settings.PRIVATE_KEY
    my_address: str = settings.BCS_ADDRESS

    @classmethod
    def hex2tx(cls, raw):
        return cls.network.tx.from_hex(raw)

    @classmethod
    def _get_spendable(cls):
        utxo = get_utxo()[0]
        raw = get_raw_tx(utxo['transactionId'])
        tx = cls.hex2tx(raw)
        return tx.tx_outs_as_spendable()[utxo['outputIndex']]

    @classmethod
    @log_error(InsufficientFunds, 'Not enough coins to make Transaction.')
    def create_signed_tx_for_new_address(cls, coins):
        new_address = get_new_address()
        spendable = cls._get_spendable()
        total_value = coins * cls.coin_mul
        residue = spendable.coin_value - total_value - cls.fee
        if residue < 0:
            raise InsufficientFunds()
        new_tx = cls.network.tx_utils.create_signed_tx(
            [spendable], [(new_address, total_value),
                          (cls.my_address, residue)],
            wifs=[cls.wif],
            fee=0)

        return new_tx


@log_error(RequestError, 'Fail to fetch new address')
def get_new_address():
    response = make_rpc_request('getnewaddress')
    return response['result']


@log_error(RequestError, 'Fail to send raw transaction')
def send_raw_transaction(raw_tx: List[str]):
    response = make_rpc_request('sendrawtransaction', params=raw_tx)
    return response['result']


@log_error(RequestError, 'Fail to get Transaction by id.')
def get_raw_tx(id: str):
    url = f'{settings.BCS_API}/raw-tx/{id}'
    raw_tx = HttpRequester.get(url)
    return raw_tx.text


@log_error(RequestError, 'Fail to get UTXO.')
def get_utxo():
    url = f'{settings.BCS_API}/address/{settings.BCS_ADDRESS}/utxo'
    utxo = HttpRequester.get(url)
    return utxo.json()
