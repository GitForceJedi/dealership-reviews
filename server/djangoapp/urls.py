from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

app_name = 'djangoapp'
urlpatterns = [
    # route is a string contains a URL pattern
    # view refers to the view function
    # name the URL
    path(route='static-template/', view=views.static_template_view, name='static_template'),

    # path for about view
    path(route='about/', view=views.about, name='about'),

    # path for contact us view
    path(route='contact/', view=views.contact, name='contact'),


    # path for registration
    path(route='registration/', view=views.registration_request, name='registration'),

    # path for login
    path(route='login/', view=views.login_request, name='login'),

    # path for logout
    path(route='logout/', view=views.logout_request, name='logout'),
    
    # path for signup
    path(route='signup/', view=views.signup, name='signup'),


    path(route='', view=views.get_dealerships, name='index'),

    # path for dealer reviews view
    path('dealer/<int:dealer_id>/', views.get_dealer_details, name='dealer_details'),

    # path for add a review view
    path('dealer/<int:dealer_id>/add_review/', views.add_review, name='add_review'),

    # path('dealer/<int:dealer_id>/', views.get_dealer_details, name='dealer_details'),
    path('dealer/info/<int:dealer_id>/', views.dealer_by_id_view, name='dealer_by_id'),

    path('dealer/info/<str:state>/', views.dealers_by_state_view, name='dealer_by_state'),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)