from django.urls import path, include
from django.contrib.auth import views as auth_views
from .views import home, add_comment, signup

urlpatterns = [
    path('', home, name='index'),
    path('captcha/', include('captcha.urls')),
    path('add-comment/', add_comment, name='add_comment'),
    path('add-comment/<int:parent_id>/', add_comment, name='add_reply'),

    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='index'), name='logout'),
    path('signup/', signup, name='signup'),
]
