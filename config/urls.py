from django.conf import settings
from django.urls import include, path
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic import TemplateView
from django.views import defaults as default_views

import stock_sentiment_web_app.sentiment.views as sentiment_views

urlpatterns = [
    path("sentiment", include("stock_sentiment_web_app.sentiment.urls"), name='sentiment'),
    path("about/", TemplateView.as_view(template_name="pages/about.html"), name="about"),
    path("", TemplateView.as_view(template_name="pages/home.html"), name="home"),
                  # Django Admin, use {% url 'admin:index' %}
    path(settings.ADMIN_URL, admin.site.urls),
    path(settings.ADMIN_URL+"/scrape", sentiment_views.scrape_data, name='scrape_data'),
    # User management
    path("users/", include("stock_sentiment_web_app.users.urls", namespace="users")),
    path("accounts/", include("allauth.urls")),
    # Your stuff: custom urls includes go here
    # path("sentiment/", include("stock_sentiment_web_app.sentiment.urls", namespace="sentiment"))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        path(
            "400/",
            default_views.bad_request,
            kwargs={"exception": Exception("Bad Request!")},
        ),
        path(
            "403/",
            default_views.permission_denied,
            kwargs={"exception": Exception("Permission Denied")},
        ),
        path(
            "404/",
            default_views.page_not_found,
            kwargs={"exception": Exception("Page not Found")},
        ),
        path("500/", default_views.server_error),
    ]
    if "debug_toolbar" in settings.INSTALLED_APPS:
        import debug_toolbar

        urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns
