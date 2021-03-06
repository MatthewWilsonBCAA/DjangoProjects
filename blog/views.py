from django.views.generic import ListView, DetailView, View
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy, resolve
from django.db.models import Count, Q
from .models import Post, Comment, Vote
from accounts.models import CustomUser
import datetime, markdown


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
        try:
            result = []
            sk = list(sort_by_n)
            for i in sk:
                if i == "&":
                    break
                result.append(i)
            sort_by_n = "".join(result)

        except:
            sort_by_n = "new"
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


class SearchView(OrderingByQueryParams, ListView):
    model = Post
    template_name = "search.html"

    def get_queryset(self):
        query = self.request.GET.get("q")  # tag__icontains=

        if not query:
            query = " "
        if "!tag!" in query:
            query = query.replace("!tag!", "")
            object_list = Post.objects.filter(Q(tag__icontains=query))
        elif "!title!" in query:
            query = query.replace("!title!", "")
            object_list = Post.objects.filter(Q(title__icontains=query))
        else:
            object_list = Post.objects.filter(
                Q(tag__icontains=query)
                | Q(title__icontains=query)
                | Q(body__icontains=query)
            )
        return object_list


class BlogListView(OrderingByQueryParams, ListView):
    queryset = Post.objects.all().annotate(num_votes=Count("votes"))
    template_name = "home.html"
    # slug_field = "sort_by"
    # slug_url_kwarg = "sort_by"
    # context_object_name = "sortby"
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        sort_by_n = self.request.GET.get("sortby")
        try:
            result = []
            sk = list(sort_by_n)
            for i in sk:
                if i == "&":
                    break
                result.append(i)
            sort_by_n = "".join(result)
            context["cursort"] = sort_by_n
        except:
            context["cursort"] = "new"
        if not context["cursort"]:
            context["cursort"] = "new"
        return context


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
        context["post_markdown"] = markdown.markdown(self.object.body)
        return context


class MakeVoteView(LoginRequiredMixin, CreateView):
    model = Vote
    fields = []

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post_id = self.request.resolver_match.kwargs["pk"]
        return super().form_valid(form)


class MakeCommentView(LoginRequiredMixin, CreateView):
    model = Comment
    template_name = "comment_new.html"
    fields = ["comment"]

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post_id = self.request.resolver_match.kwargs["pk"]
        return super().form_valid(form)


class EditCommentView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    template_name = "comment_edit.html"
    fields = ["comment"]

    def test_func(self):
        return self.get_object().author.id == self.request.user.id


class DeleteCommentView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = "comment_delete.html"
    success_url = reverse_lazy("home")
    
    def test_func(self):
        return self.get_object().author.id == self.request.user.id


class BlogCreateView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = "post_new.html"
    fields = ["title", "body", "tag"]

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.created = datetime.datetime.now()
        return super().form_valid(form)


class BlogUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    template_name = "post_edit.html"
    fields = ["title", "body", "tag"]
    def test_func(self):
        return self.get_object().author.id == self.request.user.id


class BlogDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = "post_delete.html"
    success_url = reverse_lazy("home")
    def test_func(self):
        return self.get_object().author.id == self.request.user.id


class UpdateBioView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = CustomUser
    template_name = "bio_edit.html"
    fields = ["profile_picture_link", "bio"]
    # success_url = reverse_lazy("")
    def get_success_url(self):
        return self.request.user.username

    def get_object(self):
        return self.request.user
    def test_func(self):
        return self.get_object().id == self.request.user.id


class FollowUser(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
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
        