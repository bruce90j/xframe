import xumm
import json
import xrpl.transaction
from xrpl.asyncio.clients import XRPLRequestFailureException
from xrpl.clients import JsonRpcClient

from django.conf import settings

def create_signin_payload():
    signin_payload = {
        'options': {
            'expire': 5,
        },
        'txjson': {
            'TransactionType': 'SignIn'
        }
    }
    sdk = xumm.XummSdk(settings.XUMM_API_KEY, settings.XUMM_API_SECRET)
    create_payload_resp = sdk.payload.create(signin_payload)
    return create_payload_resp.refs.qr_png, create_payload_resp.next.always, create_payload_resp.refs.websocket_status
# pong = sdk.ping()
# print(pong.application.name)


def get_user_from_signin_payload(uuid):
    sdk = xumm.XummSdk(settings.XUMM_API_KEY, settings.XUMM_API_SECRET)
    payload = sdk.payload.get(uuid)
    return payload.response.account, payload.application.issued_user_token


def get_payload(uuid):
    sdk = xumm.XummSdk(settings.XUMM_API_KEY, settings.XUMM_API_SECRET)
    payload = sdk.payload.get(uuid)
    return json.dumps(payload.to_dict(), indent=4)


def verify_transaction(tx_hash):
    JSON_RPC_URL = "https://s2.ripple.com:51234/"
    client = JsonRpcClient(JSON_RPC_URL)
    try:
        tx = xrpl.transaction.get_transaction_from_hash(tx_hash=tx_hash, client=client)
    except XRPLRequestFailureException as e:
        tx = e
        return tx

    return json.dumps(tx.to_dict(), indent=4)
    # return json.dumps(payload.to_dict(), indent=4)


def cancel_payload(uuid):
    sdk = xumm.XummSdk(settings.XUMM_API_KEY, settings.XUMM_API_SECRET)
    payload = sdk.payload.cancel(uuid)
    return payload.result.cancelled



# sdk.payload.cancel('b1001def-79f5-4b3b-baad-ae525f99f47e')
