from django.urls import path
from .views import (
    BlogListView,
    BlogDetailView,
    BlogCreateView,
    BlogUpdateView,
    BlogDeleteView,
    MakeCommentView,
    MakeVoteView,
    UserProfileView,
    UserPostsView,
    UpdateBioView,
)

urlpatterns = [
    path("post/<int:pk>/delete/", BlogDeleteView.as_view(), name="post_delete"),
    path("post/<int:pk>/edit/", BlogUpdateView.as_view(), name="post_edit"),
    path("post/new/", BlogCreateView.as_view(), name="post_new"),
    path("post/<int:pk>/", BlogDetailView.as_view(), name="post_detail"),
    path("post/<int:pk>/comment", MakeCommentView.as_view(), name="comment_new"),
    path("post/<int:pk>/vote", MakeVoteView.as_view(), name="post_vote"),
    path(
        "user/<str:username>/",
        UserProfileView.as_view(),
        name="user_profile",
    ),
    path(
        "user/<str:username>/posts",
        UserPostsView.as_view(),
        name="user_posts",
    ),
    path(
        "user/edit-bio",
        UpdateBioView.as_view(),
        name="edit_bio",
    ),
    path("<str:sort_by>/", BlogListView.as_view(), name="home"),
]