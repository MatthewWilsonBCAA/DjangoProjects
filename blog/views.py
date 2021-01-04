from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, resolve
from .models import Post, Comment


# Create your views here.


class BlogListView(ListView):
    model = Post
    template_name = "home.html"


class BlogDetailView(DetailView):
    model = Post
    template_name = "post_detail.html"


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
