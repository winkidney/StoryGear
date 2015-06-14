from django.conf.urls import include, url
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm
from storygear.sgear.views import StoryHomeView, SingleStoryView, NewStoryView, EditStoryView, NewChapterView
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm

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
            'template_name': 'account/login.html',
            'redirect_field_name': 'next',
        },
    ),
    url('^register/$', CreateView.as_view(
        template_name='accounts/register.html',
        form_class=UserCreationForm,
        # success_url='/',
    )),
    url('', include('django.contrib.auth.urls')),

)
