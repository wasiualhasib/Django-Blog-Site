from django.urls import path
from .views import (
    PostListView,
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
    MyPostListView,
    DraftPostListView,
    UserPostListView,UpdateComment)
from . import views

urlpatterns = [
    path('', PostListView.as_view(), name='blog-home'),
    path('user/<str:username>', UserPostListView.as_view(), name='user-posts'),
    # path('post/mypost/<str:username>', MyPostListView.as_view(), name='my-blog-post'),
    path('post/mypost/', MyPostListView.as_view(), name='my-blog-post'),
    
    path('post/draftpost/', DraftPostListView.as_view(), name='draft-post'),
    
    path('post/post-publish/<str:pk>/<str:url_name>', views.PublishPost, name='publish-post'),
    path('post/post-unPublish/<str:pk>/<str:url_name>', views.UnPublishPost, name='un-publish-post'),
    
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    
    path('post/<int:pk>/add-comment/',views.add_comments_to_post,name='add-comment'),
    path('post/<int:pk>/remove-comment/',views.remove_comments,name='remove-comment'),
    path('post/<int:pk>/approve-comment/',views.publish_comments,name='approve-comment'),
    path('post/<int:pk>/update-comment/',UpdateComment.as_view(),name='update-comment'),
    
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('about/', views.about, name='blog-about')
]
