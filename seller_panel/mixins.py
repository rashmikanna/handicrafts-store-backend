# mixins for seller_panel

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied

class ApprovedSellerRequiredMixin(LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        user = request.user
        if (
            not hasattr(user, 'profile')
            or user.profile.role != 'producer'
            or not hasattr(user, 'sellerprofile')
            or not user.sellerprofile.approved
        ):
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

