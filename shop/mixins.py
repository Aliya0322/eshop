from django.shortcuts import redirect
from django.contrib.auth.mixins import AccessMixin


class IsAuthenticatedMixin(AccessMixin):
    # def dispatch(self, request, *args, **kwargs):
    #     if not request.user.is_authenticated:
    #         return redirect('main-page')


    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data["is_authenticated"] = self.request.user.is_authenticated
        return data
