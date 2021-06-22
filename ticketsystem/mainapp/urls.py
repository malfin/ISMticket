from django.urls import path
import mainapp.views as mainapp

app_name = 'mainapp'

urlpatterns = [
    path('', mainapp.index, name='index'),
    path('tickets/', mainapp.my_ticket, name='my_ticket'),
    path('tickets/create/', mainapp.create_ticket, name='create_ticket'),
    path('tickets/open/<int:pk>/', mainapp.open_ticket, name='open_ticket'),
    path('tickets/close/<int:pk>/', mainapp.close_ticket, name='close_ticket'),
    path('tickets/send/<int:pk>/', mainapp.send_message, name='send_message'),

    path('profile/', mainapp.profile, name='profile'),
    path('profile/edit/', mainapp.edit_profile, name='edit_profile'),
    path('profile/edit/password/', mainapp.change_password, name='change_password'),

    path('news/', mainapp.news, name='news'),
    path('news/add/', mainapp.create_news, name='create_news'),
    path('news/edit/<int:pk>/', mainapp.edit_news, name='edit_news'),
    path('news/remove/<int:pk>/', mainapp.remove_news, name='remove_news'),

    path('ticket/admin/', mainapp.ticket_admin, name='ticket_admin'),
    path('ticket/admin/open/<int:pk>/', mainapp.open_ticket_admin, name='open_ticket_admin'),
    path('ticket/admin/send/<int:pk>/', mainapp.send_message_admin, name='send_message_admin'),
    path('ticket/admin/close/<int:pk>/', mainapp.close_ticket_admin, name='close_ticket_admin'),

    path('userprofile/', mainapp.all_users, name='all_users'),
    path('userprofile/edit/<int:pk>/', mainapp.edit_profile_admin, name='edit_profile_admin'),
    path('userprofile/add/', mainapp.create_user, name='create_user'),
]
