from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from . import views

urlpatterns = [
    path('', views.index),
    path('posts/', views.PostsApiView.as_view()),
    path('post/<slug:slug>', views.PostDetailApiView.as_view(),name="post_detail"),
    path('posts/category/<str:category>',views.GetPostBycategory.as_view()),
    path('trending',views.TrendingPosts.as_view()),
    path('latest',views.LatestPosts.as_view()),
    path('create_post/',views.CreatePostView.as_view()),
    path('edit_post/<slug:slug>',views.EditDeletePostView.as_view()),
    path('comment/<slug:slug>',views.CreateComment.as_view()),
    path('comment/',views.CreateComment.as_view()),
    path('featured-category',views.get_featured_category),
]


urlpatterns = urlpatterns + \
    static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
