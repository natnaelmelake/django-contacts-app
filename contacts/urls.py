from django.urls import path
from contacts import views
from django.contrib.auth.views import LoginView  , LogoutView 
from django.views.generic.base import RedirectView

urlpatterns = [
    path('', RedirectView.as_view(pattern_name='login', permanent=False)),
    path('register',views.register_view,name='register'),
    # path('login/', LoginView.as_view(template_name='contacts/login.html'),name='login'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'),name='logout'),
    path('home/',views.home,name='home'),
    path('list_contacts/',views.ContactListView.as_view(),name='listofcontacts'),
    path('add_contact/',views.addContact,name='add_contact'),
    path('delete_contact/<int:contact_id>',views.deleteContact,name='delete_contact'),
    path('edit_contact/<int:contact_id>',views.editContact,name='edit_contact'),
    path('search_contacts/',views.searchContacts,name='searchcontacts')

    ]
