from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, resolve
from django.db.models import Count
from .models import Post, Comment, Vote
from accounts.models import CustomUser


# Create your views here.


class BlogListView(ListView):
    model = Post
    template_name = "home.html"

    paginate_by = 25

    def get_queryset(self):
        return (
            Post.objects.all().annotate(num_votes=Count("votes")).order_by("-num_votes")
        )


class UserPostsView(ListView):
    model = CustomUser
    template_name = "user_posts.html"
    slug_field = "username"
    slug_url_kwarg = "username"
    context_object_name = "user"

    def get_queryset(self):
        cur_user = self.request.resolver_match.kwargs["username"]
        return Post.objects.filter(author__username=cur_user)


class UserProfileView(DetailView):
    model = CustomUser
    template_name = "user_profile.html"
    slug_field = "username"
    slug_url_kwarg = "username"
    context_object_name = "user"


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
        return super().form_valid(form)


class BlogUpdateView(UpdateView):
    model = Post
    template_name = "post_edit.html"
    fields = ["title", "body"]


class BlogDeleteView(DeleteView):
    model = Post
    template_name = "post_delete.html"
    success_url = reverse_lazy("home")
