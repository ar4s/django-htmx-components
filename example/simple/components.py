
from django.contrib.auth import authenticate, login, logout
from django.http import HttpRequest

from django_htmx_components import ComponentContext, htmx_components
from django_htmx_components.types import Trigger

from .forms import LoginForm


@htmx_components.register(scope="auth", name="logout_button")
def logout_button(request: HttpRequest, params):
    print("logout_button", params)
    if params.get("logout"):
        logout(request)
        return ComponentContext({}, Trigger(full_refresh=True))
    return ComponentContext({})


@htmx_components.register(scope="auth", name="login_button")
def login_button(request: HttpRequest, params):
    return ComponentContext({"is_authenticated": request.user.is_authenticated})


@htmx_components.register(scope="auth", name="login_form")
def login_form(request: HttpRequest, params):
    form = LoginForm(params or None)

    if not form.is_valid():
        return ComponentContext({'form': form})

    user = authenticate(request, username=form.cleaned_data['username'], password=form.cleaned_data['password'])

    if user is not None:
        login(request, user)
        print("login success")
        return ComponentContext({}, Trigger(full_refresh=True))

    return ComponentContext({'form': form, 'error': 'Invalid credentials'})
