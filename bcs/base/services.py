from typing import Dict, List, Any
from pycoin.networks.bitcoinish import Network, create_bitcoinish_network


def __parse_kwargs(kwargs: str):
    '''
    Parse network parameters from string
    @param kwargs - 'key1=val1, key2=val2'
    '''
    parsed: Dict[str, Any] = {}
    for kwarg in kwargs.split(', '):
        item: List[str] = kwarg.split('=')
        key = item[0]
        value = item[1].strip('"')
        parsed[key] = value
    return parsed

def get_network(kwargs):
    parameters = __parse_kwargs(kwargs)
    return create_bitcoinish_network('BCS', 'BCS Chain', 'BCS Chain', **parameters)

def get_base_network() -> Network:
    kwargs = 'wif_prefix_hex="80", address_prefix_hex="19", pay_to_script_prefix_hex="32", bip32_prv_prefix_hex="0488ade4", bip32_pub_prefix_hex="0488B21E", bech32_hrp="bc", bip49_prv_prefix_hex="049d7878", bip49_pub_prefix_hex="049D7CB2", bip84_prv_prefix_hex="04b2430c", bip84_pub_prefix_hex="04B24746", magic_header_hex="F1CFA6D3", default_port=3666'
    return get_network(kwargs)

if __name__ == "__main__":
    network = get_base_network()
    print(network.tx.coinbase_tx(b'23123', 1).as_hex())
