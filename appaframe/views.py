import json
from urllib.request import urlopen

from django.shortcuts import render, redirect
from django.views import View
from django.conf import settings

from appmain.helpers import x_helper
from appmain.permission_manager import WalletOrUserRequiredMixin


class AframeView(WalletOrUserRequiredMixin, View):
    template_path = "appaframe/aframe.html"
    page_title = "X-frame Scene"

    def get(self, request):
        nfts = []
        for nft in x_helper.get_nft(request.session['xumm_account'])['account_nfts']:
            try:
                link = bytearray.fromhex(nft['URI']).decode()
                response = urlopen(link, timeout=3)
                img = json.loads(response.read())['image_url']
                if "ipfs" in img:
                    img = 'https://ipfs.io/ipfs/' + img.split('ipfs/')[1]
                nfts.append(img)
            except:
                pass
        return render(request, self.template_path, {
            'local': settings.DEBUG,
            'my_nfts': nfts
        })