# django-htmx-components

The package is in early development stage and is not ready for production use.

The package provides a set of components for Django that can be used to build dynamic web pages using [htmx](https://htmx.org/).
A main goal of the package is to provide a set of components that can be used to build a web page without writing any JavaScript code and provide an opionionated way to build dynamic web pages.

Each component is a simple Python function that returns a dictionary with data that can be used to render a component on a page.

# Usage
Add `django_htmx_components` to `INSTALLED_APPS` in your Django settings file.

```python
INSTALLED_APPS = [
    ...
    "django_htmx_components",
    ...
]
```
Next add `htmx_components` to your `urls.py` file.
```python
from django.urls import include, path
from django_htmx_components import htmx_components

urlpatterns = [
    ...
    path("", include(htmx_components.urls)),
    ...
]
```
Add `components.py` file to your app and register components in it.
```python
from django.http import HttpRequest
from django_htmx_components import ComponentContext, htmx_components

@htmx_components.register(scope="auth", name="login_button")
def login_button(request: HttpRequest, params):
    return ComponentContext({"is_authenticated": request.user.is_authenticated})
```
`components.py` file is automatically imported by `django_htmx_components` app, so you don't need to import it anywhere else.
Render component in your regular template.

Next, you need to define template for your component.

```html
{% load i18n htmx_components_tags %}

{% if is_authenticated %}
  <p>{% translate "you are logged in!" %}</p>
{% else %}
  <button hx-trigger="click" hx-swap="outerHTML" hx-get="{% url 'htmx:component' 'auth' 'login_form' %}">{% translate "login" %}</button>
{% endif %}

```

And last but not least, you need to define template for your component.

```html
{% load i18n htmx_components_tags %}

{% htmx_component 'auth' 'login_button' %}

```
As you can see, the component is rendered using `htmx_component` template tag, so you can reuse other components inside your components.
That's it! You have a working component.

## Developer experience
For better developer experience, the package provides a "storybook" like page that can be used to see all components.
Check [example](http://localhost:8000/htmx/_scopes/auth/) to see how it looks like.

## TODO
- [ ] Add more examples
- [ ] Add tests
- [ ] Add documentation
- [ ] Add debug toolbar panel
- [ ] Add CSS to "storybook"
