import xumm
import json
import xrpl.transaction
from xrpl.asyncio.clients import XRPLRequestFailureException
from xrpl.clients import JsonRpcClient
from xrpl.models.requests import AccountNFTs
from xrpl.models.requests.account_info import AccountInfo

from django.conf import settings

sdk = xumm.XummSdk(settings.XUMM_API_KEY, settings.XUMM_API_SECRET)
xrpc = JsonRpcClient("https://s.altnet.rippletest.net:51234/")  # https://s2.ripple.com/


def create_payload(payload):
    create_payload_resp = sdk.payload.create(payload)
    return create_payload_resp.refs.qr_png, create_payload_resp.next.always, create_payload_resp.refs.websocket_status


def get_payload(uuid):
    payload = sdk.payload.get(uuid)
    # return payload.response
    return payload
    # return json.dumps(payload.to_dict(), indent=4)


def cancel_payload(uuid):
    payload = sdk.payload.cancel(uuid)
    return payload.result.cancelled


'''_______________ Account helpers ________________ '''


def create_xumm_signin():
    signin_payload = {
        'options': {
            'expire': 5,
        },
        'txjson': {
            'TransactionType': 'SignIn'
        }
    }
    return create_payload(signin_payload)


def get_xumm_user(uuid):
    payload = sdk.payload.get(uuid)
    return payload.response.account, payload.application.issued_user_token


def get_account_info(account):
    acct_info = AccountInfo(
        account=account,
        # ledger_index="validated",
        # strict=True,
    )
    response = xrpc.request(acct_info)
    return response.result
    # print("response.status: ", response.status)
    # import json
    # print(json.dumps(response.result, indent=4, sort_keys=True))


'''_______________ NFT helpers ________________ '''


def mint_nft(uri, user_token=""):
    payload = {
        'user_token': user_token,
        'options': {
            'expire': 3,
        },
        'txjson': {
            'TransactionType': 'NFTokenMint',
            'NFTokenTaxon': 0,  # for collections use the same number
            'Flags': 8,  # 8 means tradable
            'TransferFee': 1000,  # 'Fee': '10',
            'URI': uri,

        }
    }
    return create_payload(payload)


def burn_nft(token_id, user_token=""):
    payload = {
        'user_token': user_token,
        'options': {
            'expire': 3,
        },
        'txjson': {
            'TransactionType': 'NFTokenBurn',
            'NFTokenID': token_id
        }
    }
    return create_payload(payload)


def get_nft(account):
    acct_nfts = AccountNFTs(
        account=account
    )
    response = xrpc.request(acct_nfts)
    return response.result



'''_______________ Misc ________________ '''


def verify_transaction(tx_hash):
    try:
        tx = xrpl.transaction.get_transaction_from_hash(tx_hash=tx_hash, client=xrpc)
    except XRPLRequestFailureException as e:
        tx = e
        return tx
    return json.dumps(tx.to_dict(), indent=4)

'''_______________ Connector ________________ '''


def request_payload(action, data, user_token=""):
    match action:
        case "mint_nft":
            return mint_nft(data, user_token)
        case "burn_nft":
            return burn_nft(data, user_token)
        case _:
            return False
