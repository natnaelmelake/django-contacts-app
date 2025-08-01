from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import get_object_or_404, render , redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from django.views.generic import ListView
from .models import Contact
from django.views.generic.edit import CreateView
from .forms import ContactForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.contrib.auth.views import LoginView
from .forms import CustomLoginForm,CustomUserCreationForm
# Create your views here.


def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = CustomUserCreationForm()

    return render(request,'contacts/register.html',{'form':form})


class CustomLoginView(LoginView):
    authentication_form = CustomLoginForm
    template_name = 'contacts/login.html'


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required
def home(request):
    return render(request,'contacts/home.html',)



class ContactListView(LoginRequiredMixin,ListView):
    model = Contact
    template_name = 'contacts/contact_list.html'
    context_object_name = 'list_contacts'

    def get_queryset(self):
        # Optional: Show only contacts belonging to the current user
        return Contact.objects.filter(user=self.request.user)




@login_required
def addContact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            contact = form.save(commit=False)
            contact.user = request.user
            contact.save()
            return redirect('listofcontacts')
    else:
        form = ContactForm()
    return render(request, 'contacts/add_contact.html', {'form': form})

@login_required
def deleteContact(request,contact_id):
    contact = get_object_or_404(Contact,id=contact_id,user=request.user)
    contact.delete()
    return redirect('listofcontacts')


@login_required
def editContact(request,contact_id):
    contact = get_object_or_404(Contact,id=contact_id,user=request.user)
    
    if request.method == 'POST':
        form = ContactForm(request.POST,instance=contact)
        if form.is_valid():
            form.save()
            return redirect('listofcontacts')
    else:
        form = ContactForm(instance=contact)

    return render(request,'contacts/edit_contact.html',{'form':form})

    
    

@login_required
def searchContacts(request):
    query = request.GET.get('q')
    if query:
       contacts = Contact.objects.filter(
    Q(first_name__icontains=query) |
    Q(last_name__icontains=query) |
    Q(email__icontains=query) |
    Q(phone_number__icontains=query)
)
    else:
        contacts = Contact.objects.all()
    return render(request,'contacts/contact_list.html',{'list_contacts':contacts})
    







# class AddContactView(CreateView):
#     model = Contact
#     form_class = ContactForm
#     template_name = 'contacts/add_contact.html'
#     success_url = '/list_contacts/'








