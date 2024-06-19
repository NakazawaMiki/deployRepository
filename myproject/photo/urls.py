from django.urls import path
from . import views

app_name = 'photo'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('works/', views.CreateWorksView.as_view(), name='works'),
    path('works_done', views.WorksSuccessView.as_view(), name='works_done'),
    path('photos/<int:category>', views.CategoryView.as_view(), name='photos_cat'),
    path('user-list/<int:user>', views.UserView.as_view(), name='user_list'),
    path('photo-detail/<int:pk>', views.DetailView.as_view(), name='photo_detail'),
    path('mypage/', views.MypageView.as_view(), name='mypage'),
    path('photo/<int:pk>/delete/', views.PhotoDeleteView.as_view(), name = 'photo_delete'),
    path('photo/<int:pk>/like', views.LikeView.as_view(), name='photo_like'),
]

