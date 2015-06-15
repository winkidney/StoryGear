from django.conf.urls import include, url
from storygear.account.views import ProfileView
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth.views import logout

urlpatterns = (
    # url('^register/$', CreateView.as_view(
    #     template_name='account/register.html',
    #     form_class=UserCreationForm,
    #     success_url='/'
    # )),
    # url('^login/$', LoginView),
    url(
        '^login/$',
        'django.contrib.auth.views.login',
        {
            'template_name': 'accounts/login.html',
            'redirect_field_name': 'next',
        },
    ),
    url(
        '^logout/$',
        'django.contrib.auth.views.logout',
        {
            'next_page': '/',
            'redirect_field_name': 'next'
        }
    ),
    url('^register/$', CreateView.as_view(
        template_name='accounts/register.html',
        form_class=UserCreationForm,
        success_url='/story/',
    )),
    url('^profile/$', ProfileView(), name="accounts.profile"),
    url('', include('django.contrib.auth.urls')),
)
