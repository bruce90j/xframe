from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.views import View
from rest_framework.views import APIView
from rest_framework.response import Response

from django.conf import settings

from appmain.helpers import x_helper
from appmain.models import NFT
from appmain.permission_manager import WalletOrUserRequiredMixin


class IndexView(View):
    template_path = "base.html"
    page_title = "Home"

    def get(self, request):
        return render(request, self.template_path, {})


class AccountView(View):
    template_path = "appmain/account.html"
    page_title = "Profile"

    def get(self, request):
        # request.session['xumm_account'] = 'rntaS4R2KT4hbV1uNEbkYfUrW1zj6csvhQ'
        return render(request, self.template_path, { })


class ConnectWalletView(View):
    template_path = "registration/connect-wallet.html"
    page_title = "Wallet"

    def get(self, request):
        return render(request, self.template_path, {})


class ConnectXummWalletView(View):
    template_path = "registration/connect-xumm-wallet.html"
    page_title = "Xumm"

    def get(self, request):
        qr, lk, ws = x_helper.create_xumm_signin()
        return render(request, self.template_path, {
            'xumm_qr': qr,
            'xumm_lk': lk,
            'xumm_ws': ws,
        })

    def post(self, request):
        xumm_uuid = request.POST.get("xumm_uuid", "")
        account, token = x_helper.get_xumm_user(xumm_uuid)
        request.session['xumm_account'] = account
        request.session['xumm_token'] = token
        return redirect('appmain:home')


def logout_view(request):
    logout(request)
    return redirect('appmain:home')


class SignPayloadView(WalletOrUserRequiredMixin, View):
    template_path = "xumm_payload.html"
    page_title = "Sign payload"

    def get(self, request):
        payload_title = "Sign Payload"
        qr = request.GET.get("qr", "")
        lk = request.GET.get("lk", "")
        ws = request.GET.get("ws", "")
        return render(request, self.template_path, {
            'payload_title': payload_title,
            'xumm_qr': qr,
            'xumm_lk': lk,
            'xumm_ws': ws,
        })

    def post(self, request):
        xumm_uuid = request.POST.get("xumm_uuid", "")
        response = x_helper.get_payload(xumm_uuid)
        # result = response.meta.resolved and response.meta.signed and not response.meta.cancelled
        return redirect('appmain:home')


class NFTCreateView(WalletOrUserRequiredMixin, View):
    template_path = "appmain/nft-create.html"
    page_title = "Create NFT"

    def get(self, request):
        return render(request, self.template_path, { })

    def post(self, request):
        nft_name = request.POST.get("nft_name", "")
        nft_description = request.POST.get("nft_description", "")
        nft_image_url = request.POST.get("nft_image_url", "")
        nft_animation_url = request.POST.get("nft_animation_url", "")
        # TODO: push to IPFS
        nft = NFT.objects.create(name=nft_name, description=nft_description, image_url=nft_image_url, animation_url=nft_animation_url)
        uri = "{d}/nft/{xid}/".format(d=settings.HOST, xid=nft.xid).encode("utf-8").hex()
        qr, lk, ws = x_helper.mint_nft(uri, request.session['xumm_token'])
        return render(request, "xumm_payload.html", {
            'payload_title': "Mint NFT",
            'xumm_qr': qr,
            'xumm_lk': lk,
            'xumm_ws': ws,
        })


class NFTMetadataView(APIView):
    def get(self, request, xid):
        nft = NFT.objects.get(xid=xid)
        return Response({
            'name': nft.name,
            'description': nft.description,
            'image_url': nft.image_url,
            'animation_url': nft.animation_url,
            'gltf_url': nft.gltf_url,
        })