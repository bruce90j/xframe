from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.views import View
from django.conf import settings

from appmain.helpers import x_helper
from appmain.permission_manager import WalletOrUserRequiredMixin


# Create your views here.


class IndexView(View):
    template_path = "base.html"
    page_title = "Home"

    def get(self, request):
        return render(request, self.template_path, {})


class ProfileView(View):
    template_path = "appmain/profile.html"
    page_title = "Profile"

    def get(self, request):
        return render(request, self.template_path, {})


class AframeView(WalletOrUserRequiredMixin, View):
    template_path = "appmain/aframe.html"
    page_title = "X-frame Scene"

    def get(self, request):
        return render(request, self.template_path, {
            'local': settings.DEBUG,
        })


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
    page_title = "Sign transaction"

    def get(self, request):
        qr, lk, ws = x_helper.mint_nft("6148523063484D364C793930636D6C73595749755A475632", user_token=request.session['xumm_token']) # TODO: remove hardcoded mint
        return render(request, self.template_path, {
            'xumm_qr': qr,
            'xumm_lk': lk,
            'xumm_ws': ws,
        })

    def post(self, request):
        xumm_uuid = request.POST.get("xumm_uuid", "")
        response = x_helper.get_payload(xumm_uuid)
        return render(request, self.template_path, {
            'response': response,
        })
        # return redirect('appmain:home')