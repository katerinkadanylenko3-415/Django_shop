from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.timezone import now

from .forms import PostForm, LoginForm
import datetime

from .forms import PostForm
from .models import Post, Category


def get_categories():
    all = Category.objects.all()
    count = all.count()
    half = count / 2 + count % 2
    first_half = all[:half]
    second_half = all[half:]
    return {'cat_left': first_half, 'cat_right': second_half}


def index(request):
    posts = Post.objects.all().order_by("-published_date")

    context = {'posts': posts}
    context.update(get_categories())
    return render(request, "blog/index.html", context)


def contacts(request):
    context = {}
    return render(request, "blog/contact.html", context)






from .forms import PostForm, LoginForm, CommentForm


def post_detail(request, slug=None):
    post = get_object_or_404(Post, slug=slug)

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('post_detail', slug=post.slug)
    else:
        form = CommentForm()

    context = {
        'post': post,
        'form': form,
    }
    context.update(get_categories())
    return render(request, "blog/post.html", context)


# def post_detail(request, slug=None):
#     post = get_object_or_404(Post, slug=slug)
#     context = {'post': post}
#     context.update(get_categories())
#     return render(request, "blog/post.html", context)


def category(request, slug=None):
    c = get_object_or_404(Category, slug=slug)
    posts = Post.objects.filter(category=c).order_by("-published_date")
    context = {'posts': posts}
    context.update(get_categories())
    return render(request, "blog/index.html", context)


from .models import Post, Category, Tag

def tag_posts(request, slug=None):
    t = get_object_or_404(Tag, slug=slug)
    posts = Post.objects.filter(tags=t).order_by("-published_date")
    context = {'posts': posts, 'current_tag': t}
    context.update(get_categories())
    return render(request, "blog/index.html", context)


def search(request):

    query = request.GET.get("query")
    posts = Post.objects.filter(Q(content__icontains=query)|Q(title__icontains=query))

    context = {'posts': posts}
    context.update(get_categories())
    return render(request, "blog/index.html", context)

@login_required
def create_post(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.published_date = now()
            new_post.user = request.user
            new_post.save()
            form.save_m2m() # тільки для many to many зв'язку
            return index(request)
    form = PostForm()
    context = {'form': form}
    return render(request, "blog/create.html", context)


def user_login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                form.add_error(None, 'Невірний логін або пароль')




    form = LoginForm()
    context = {'form': form}
    return render(request, "registration/login.html", context)


def user_logout(request):
    logout(request)
    return render(request, "registration/logged_out.html")


@login_required
def delete_post(request, slug):
    post = get_object_or_404(Post, slug=slug, user=request.user)

    if request.method == "POST":
        post.delete()
        return redirect('home')

    context = {'post': post}
    context.update(get_categories())
    return render(request, "blog/delete_confirm.html", context)



# реєстрація користувача
from .forms import RegisterForm


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            from .models import Profile
            Profile.objects.create(user=user)

            login(request, user)
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request, "registration/register.html", {'form': form})





from .forms import ProfileEditForm


@login_required
def profile_view(request):
    from .models import Profile
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = ProfileEditForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileEditForm(instance=profile)

    context = {
        'user': request.user,
        'profile': profile,
        'form': form,
    }
    context.update(get_categories())
    return render(request, "blog/profile.html", context)


from django.shortcuts import redirect
from django.contrib import messages
from .models import Subscription


def subscribe(request):
    if request.method == "POST":
        email = request.POST.get('email')
        if not Subscription.objects.filter(email=email).exists():
            Subscription.objects.create(email=email)
            messages.success(request, "Дякуємо за підписку!")
        else:
            messages.info(request, "Ви вже підписані на наші новини.")

        return redirect(request.META.get('HTTP_REFERER', 'home'))
    return redirect('home')

