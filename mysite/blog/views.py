from django.shortcuts import render,get_object_or_404,redirect
from django.views.generic import (TemplateView,ListView,DetailView,
CreateView,UpdateView,DeleteView)
# from django.views.generic.edit import FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from blog.models import Post,Comment
from blog.forms import PostForm,CommentForm,UserForm
from django.utils import timezone
from django.urls import reverse_lazy

# Create your views here.

class AboutView(TemplateView):
    template_name = 'about.html'

class PostListView(ListView):

    model = Post

    def get_queryset(self):
        return Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')


class PostDetailView(DetailView):

    model = Post


class CreatePostView(LoginRequiredMixin,CreateView):

    login_url = '/login/'

    redirect_field_name = 'blog/post_detail.html'

    form_class = PostForm

    model = Post

class PostUpdateView(LoginRequiredMixin,UpdateView):

    login_url = '/login/'

    redirect_field_name = 'blog/post_detail.html'

    form_class = PostForm

    model = Post


class PostDeleteView(LoginRequiredMixin,DeleteView):

    model = Post

    success_url = reverse_lazy('post_list')


class DraftListView(LoginRequiredMixin,ListView):

    login_url = '/login/'

    redirect_field_name = 'blog/post_list.html'

    model = Post

    def get_queryset(self):
        return Post.objects.filter(published_date__isnull=True).order_by('created_date')


def register(request):

    registered = False

    if request.method == "POST":
        userform = UserForm(request.POST)
        # profileform = UserProfileInfoForm(request.POST)

        if userform.is_valid():

            user = userform.save(commit=False)

            username =  userform.cleaned_data.get('username')
            raw_password1 = userform.cleaned_data.get('password1')
            raw_password2 = userform.cleaned_data.get('password2')
            email = userform.cleaned_data.get('email')

            if raw_password1 == raw_password2:

                user.set_password(userform.cleaned_data['password1'])
                user.is_superuser = True
                user.is_staff = True
                user.save()
                registered = True

                return redirect('login')

            else:
                print(userform.errors)

        else:
            print(userform.errors)
    else:
        userform = UserForm()

    return render(request,'blog/register.html',{'userform':userform,'registered':registered})


###############################################################
##############################################################
@login_required
def add_comment_to_post(request,pk):

    post = get_object_or_404(Post,pk=pk)

    if request.method == "POST":

        form = CommentForm(request.POST)

        if form.is_valid():

            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('post_detail',pk=post.pk)
    else:
        form = CommentForm()

    return render(request,'blog/comments_form.html',{'form':form})

@login_required
def comment_approve(request,pk):

    comment = get_object_or_404(Comment,pk=pk)
    comment.approve()
    return redirect('post_detail',pk=comment.post.pk)


@login_required
def comment_remove(request,pk):

    comment = get_object_or_404(Comment,pk=pk)
    post_pk = comment.post.pk
    comment.delete()
    return redirect('post_detail',pk=post_pk)


@login_required
def post_publish(request,pk):
    post = get_object_or_404(Post,pk=pk)
    post.publish()
    return redirect('post_detail',pk=pk)
