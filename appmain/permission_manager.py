from django.contrib.auth.mixins import PermissionRequiredMixin


class WalletOrUserRequiredMixin(PermissionRequiredMixin):
    def has_permission(self):
        xumm_session = self.request.session.get('xumm_token', False)
        # user_authenticated = self.request.user.is_authenticated
        return xumm_session # or user_authenticated
