"""root URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from . import views
from root import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^$', views.HomeView.as_view(), name='home'),
    url(r'^add_story$', views.AddStoryView.as_view(), name='add_story'),
    url(r'^view_story/(?P<story_temp_id>.+)$', views.ViewStoryView.as_view(), name='view_story'),
    url(r'^pick_story$', views.PickStoryView.as_view(), name='pick_story'),
    url(r'^story/comment$', views.StoryCommentView.as_view(), name='story_comment'),
    url(r'^select_group$', views.SelectGroupView.as_view(), name='select_group'),
]

if settings.DEBUG is True:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
