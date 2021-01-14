from django.views.generic import ListView, DetailView, View
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, resolve
from django.db.models import Count
from .models import Post, Comment, Vote
from accounts.models import CustomUser
import datetime


# Create your views here.
class GettingStartedView(ListView):
    model = Post
    template_name = "start.html"


class UserListView(ListView):
    model = CustomUser
    template_name = "user_list.html"


class OrderingByQueryParams:
    def get_ordering(self):
        sort_by_n = self.request.GET.get("sortby")
        print(sort_by_n)
        if sort_by_n == "top":
            return "-num_votes"
        else:
            return "-created"


class ShowLeaderPosts(OrderingByQueryParams, ListView):
    model = Post
    template_name = "following.html"

    def get_queryset(self):
        return Post.objects.filter(author__followers=self.request.user).order_by(
            "-created"
        )


class BlogListView(OrderingByQueryParams, ListView):
    queryset = Post.objects.all().annotate(num_votes=Count("votes"))
    template_name = "home.html"
    # slug_field = "sort_by"
    # slug_url_kwarg = "sort_by"
    # context_object_name = "sortby"
    # paginate_by = 25

    # return Post.objects.all().


class UserPostsView(OrderingByQueryParams, ListView):
    model = CustomUser
    template_name = "user_posts.html"
    slug_field = "username"
    slug_url_kwarg = "username"
    context_object_name = "currently_viewing_user"

    def get_queryset(self):
        cur_user = self.request.resolver_match.kwargs["username"]
        return Post.objects.filter(author__username=cur_user)


class UserProfileView(DetailView):
    model = CustomUser
    template_name = "user_profile.html"
    slug_field = "username"
    slug_url_kwarg = "username"
    context_object_name = "currently_viewing_user"


class BlogDetailView(DetailView):
    model = Post
    template_name = "post_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context["user_has_voted"] = (
                context["post"].votes.filter(author=self.request.user).exists()
            )
        else:
            context["user_has_voted"] = True

        return context


class MakeVoteView(CreateView):
    model = Vote
    fields = []

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post_id = self.request.resolver_match.kwargs["pk"]
        return super().form_valid(form)


class MakeCommentView(CreateView):
    model = Comment
    template_name = "comment_new.html"
    fields = ["comment"]

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post_id = self.request.resolver_match.kwargs["pk"]
        return super().form_valid(form)


class BlogCreateView(CreateView):
    model = Post
    template_name = "post_new.html"
    fields = ["title", "body"]

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.created = datetime.datetime.now()
        return super().form_valid(form)


class BlogUpdateView(UpdateView):
    model = Post
    template_name = "post_edit.html"
    fields = ["title", "body"]


class BlogDeleteView(DeleteView):
    model = Post
    template_name = "post_delete.html"
    success_url = reverse_lazy("home")


class UpdateBioView(UpdateView):
    model = CustomUser
    template_name = "bio_edit.html"
    fields = ["profile_picture_link", "bio"]
    # success_url = reverse_lazy("")
    def get_success_url(self):
        return self.request.user.username

    def get_object(self):
        return self.request.user


class FollowUser(UpdateView):
    model = CustomUser
    fields = []
    slug_field = "username"
    slug_url_kwarg = "username"
    context_object_name = "currently_viewing_user"
    success_url = reverse_lazy("home")

    def form_valid(self, form):

        cur_username = self.request.resolver_match.kwargs["username"]
        cur_user = CustomUser.objects.get(username=cur_username)
        self.request.user.leaders.add(cur_user)
        # act_user = CustomUser.objects.get(username=self.request.user.username)
        # cur_user.followers.add()

        return super().form_valid(form)