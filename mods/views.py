from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.http import HttpResponse
from hitcount.views import HitCountDetailView
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post
from .filters import PostFilter
from django.core.paginator import Paginator
from django.shortcuts import render


def home(request):
    context = {
    'posts': Post.objects.all()
    }
    return render(request, 'mods/home.html', context)

class FilteredListView(ListView):
    filterset_class = None

    def get_queryset(self):
        # Get the queryset however you usually would.  For example:
        queryset = super().get_queryset()
        # Then use the query parameters and the queryset to
        # instantiate a filterset and save it as an attribute
        # on the view instance for later.
        self.filterset = self.filterset_class(self.request.GET, queryset=queryset)
        # Return the filtered queryset
        return self.filterset.qs.distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Pass the filterset to the template - it provides the form.
        context['filterset'] = self.filterset
        return context


class PostListView(FilteredListView):
    filterset_class = PostFilter
    model = Post
    template_name = "mods/home.html"
    context_object_name = "posts"
    ordering = ["-date_posted"]
    paginate_by = 6

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset())
        return context

class UserPostListView(ListView):
    model = Post
    template_name = "mods/user_posts.html"
    context_object_name = "posts"
    ordering = ["-date_posted"]
    paginate_by = 6

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get("username"))
        return Post.objects.filter(author=user).order_by("-date_posted")

class PostDetailView(HitCountDetailView):
    model = Post
    count_hit = True

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ["title", "description", "content", "thumbnail", "category", "version", "download", "tags", "website"]

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def upload_pic(request):
        if request.method == 'POST':
            form = form(request.POST, request.FILES)
        if form.is_valid():
            m = Post.objects.get(pk=course_id)
            m.model_pic = form.cleaned_data['image']
            m.save()

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ["title", "description", "content", "thumbnail", "category", "version", "download", "tags", "website"]

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

    def upload_pic(request):
        if request.method == 'POST':
            form = form(request.POST, request.FILES)
        if form.is_valid():
            m = Post.objects.get(pk=course_id)
            m.model_pic = form.cleaned_data['image']
            m.save()


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = "/"

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


def rewards(request):
    return render(request, 'mods/rewards.html', {"title": "Rewards"})

def faq(request):
    return render(request, 'mods/faq.html', {"title": "FAQ"})
