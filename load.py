from plenum.client.client import *
from stp_core.network.port_dispenser import genHa
from stp_core.loop.looper import Looper
from plenum.test.helper import *
from time import *
from plenum.common.signer_simple import SimpleSigner

numReqs = 5000
splits = 5


def load():
    port = genHa()[1]
    ha = HA('0.0.0.0', port)
    name = "hello"
    wallet = Wallet(name)
    wallet.addIdentifier(
        signer=SimpleSigner(seed=b'000000000000000000000000Steward1'))
    client = Client(name, ha=ha)
    with Looper(debug=True) as looper:
        looper.add(client)
        print('Will send {} reqs in all'.format(numReqs))
        requests = sendRandomRequests(wallet, client, numReqs)
        start = perf_counter()
        for i in range(0, numReqs, numReqs // splits):
            print('Will wait for {} now'.format(numReqs // splits))
            s = perf_counter()
            checkSufficientRepliesForRequests(looper, client, requests[
                                                              i:i + numReqs // splits + 1],
                                              2, 3)
            print('>>> Got replies for {} requests << in {}'.
                  format(numReqs // splits, perf_counter() - s))
        end = perf_counter()
        print('>>>{}<<<'.format(end - start))
        exit(0)


if __name__ == "__main__":
    load()
