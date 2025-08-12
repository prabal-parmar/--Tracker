from django.urls import path
from tracker import views
urlpatterns = [
    path('', views.index, name="index"),
    path('login', views.loginUser, name="login"),
    path('logout', views.logoutUser, name="logout"),
    path('register', views.register, name="register"),
    path('profile', views.profile, name="profile"),
    path('profile/update', views.updateProfile, name="updateProfile"),
    path('about', views.about, name="about"),
    path('totalexpense', views.allExpenses, name="allExpenses"),
    path('delete/<uuid:id>', views.deleteExpense, name="deleteExpense"),
    path('update/<uuid:id>', views.updateExpense, name="updateExpense"),
]