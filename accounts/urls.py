from django.conf.urls import url
from django.urls import path
from . import views
from django.views.generic import TemplateView
from . import calendar_views as calviews
app_name = "accounts"

urlpatterns = [
    path('change-password', views.change_password, name='password-change'),
    path('<slug:club_name>/list-for-president/', views.listForPresident, name='list_for_president'),
    path('<slug:club_name>/list-for-moderator/', views.listForModerator, name='list_for_moderator'),
    path('makeMember/', views.makeMember, name='make_member'),
    path('makeModerator/', views.makeModerator, name='make_moderator'),
    path('profile/', views.profile, name='profile'),

    # Calendar urls
    url(r'^calendar/next/(?P<select>\w+)/(?P<show>\w+)/$', calviews.date, name='date'),
    # path('next/<select>/',views.date,name = "date"),
    # path('back/<select>/',views.date1,name = "date1"),
    url(r'^calendar/back/(?P<select>\w+)/(?P<show>\w+)/$', calviews.date1, name='date1'),
    path('events_enter/<int:date_selected>', calviews.event_enter, name="event_enter"),
    url(r'^calendar/land/(?P<select>\w+)/(?P<show>\w+)/$', calviews.hello, name='index'),
    url(r'^calendar/choose/(?P<select>\w+)/(?P<show>\w+)/$', calviews.choose_event, name='choose'),
]
