from django.contrib import admin
from django.urls import path,include
from ipl import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home),
    path('predict/',views.home1, name='model1'),
    path('winning_probability/',views.home2, name='model2'),
    path('predict/PREDICT',views.result1),
    path('winning_probability/PROBABILITY/',views.result2)
]