from django.shortcuts import redirect
from shop.forms import CustomUserCreationForm
from django.http import HttpRequest

class IsAuthenticatedMixin:
    def register_page(request: HttpRequest):
        if request.method == "POST":
            form = CustomUserCreationForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect("main-page")

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data["is_authenticated"] = self.request.user.is_authenticated
        return data
