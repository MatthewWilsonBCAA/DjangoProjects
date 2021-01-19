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
    GettingStartedView,
    UserListView,
    ShowLeaderPosts,
    FollowUser,
    SearchView,
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
    path("user/<str:username>/follow", FollowUser.as_view(), name="user_follow"),
    path(
        "user/edit-bio",
        UpdateBioView.as_view(),
        name="edit_bio",
    ),
    # path("list/", UserListView.as_view(), name="user_list"),
    path("following/", ShowLeaderPosts.as_view(), name="following"),
    path("search/", SearchView.as_view(), name="search"),
    path("", BlogListView.as_view(), name="home"),
    # path("", GettingStartedView.as_view(), name="start"),
]