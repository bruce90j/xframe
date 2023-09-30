const network = "wss://s.altnet.rippletest.net:51233/"

async function loadAccountBalances(address) {
    const client = new xrpl.Client(network)
    await client.connect()
    const balances = await client.getBalances(address);
    await client.disconnect()
    return balances
}

async function loadAccountNFTs(address) {
    const client = new xrpl.Client(network)
    await client.connect()
    const request = {
        command: "account_nfts",
        account: address,
    };
    const accountNFTs = await client.request(request);
    console.info('nfts', accountNFTs);
    const nfts = accountNFTs.result.account_nfts;
    await client.disconnect()
    return nfts
}

async function fetchNFTMetadata(uri) {
    try {
        const response = await fetch(uri);
        const data = await response.json();
        return data
    } catch (error) {
        console.log(error);
    }
}


// TOOLS ______________________________
function hex2a(hexx) {
    var hex = hexx.toString();
    var str = '';
    for (var i = 0; i < hex.length; i += 2)
        str += String.fromCharCode(parseInt(hex.substr(i, 2), 16));
    return str;
}

function a2hex(str) {
    var arr = [];
    for (var i = 0, l = str.length; i < l; i++) {
        var hex = Number(str.charCodeAt(i)).toString(16);
        arr.push(hex);
    }
    return arr.join('');
}