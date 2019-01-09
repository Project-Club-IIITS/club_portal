from time import sleep

from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.
from base.models import Club, ClubModerator
from posts.forms import PostFilterForm, PostCreationForm, PostUpdateForm
from posts.models import PinnedPost, Post


@login_required
def posts(request):
    following_clubs = request.user.userprofile.following_clubs.all()
    following_clubs_id = [club.id for club in following_clubs]


    posts = Post.objects.filter(is_approved=True).filter(club__id__in=following_clubs_id)
    print(posts)
    top_3_posts = posts.order_by('-votes')[:3]

    pinned_posts = PinnedPost.objects.all()[:3]

    post_filter_form = PostFilterForm(request.GET)

    post_filter_form.is_valid()
    # Make sure to call clean()

    page = 1
    if 'page' in post_filter_form.cleaned_data:
        if post_filter_form.cleaned_data['page']:
            page = post_filter_form.cleaned_data['page']


    paginator = Paginator(posts, 3)
    try:
        posts_page = paginator.page(page)

        if page != 1:
            sleep(1.2)
    except PageNotAnInteger:
        posts_page = paginator.page(1)
    except EmptyPage:
        posts_page = paginator.page(paginator.num_pages)

    return render(request, "posts/general_post.html",
                  {"posts": posts_page,
                   "top_posts": top_3_posts,
                   "filter_form": post_filter_form,
                   "pinned_posts": pinned_posts,
                   })





@login_required
def club_posts(request, club_name_slug):
    club_name = club_name_slug.replace('-', ' ')
    club = get_object_or_404(Club, name=club_name)

    posts = club.post_set.filter(club=club, is_approved=True)

    top_3_posts = posts.order_by('-votes')[:3]

    pinned_posts = PinnedPost.objects.filter(post__club=club)

    post_filter_form = PostFilterForm(request.GET)

    post_filter_form.is_valid()
    # Make sure to call clean()

    page = 1
    if 'page' in post_filter_form.cleaned_data:
        if post_filter_form.cleaned_data['page']:
            page = post_filter_form.cleaned_data['page']

    # Add more conditions on post_filter_form here

    # TODO Add a check here to make sure only public posts are shown to user is not a member of the club

    paginator = Paginator(posts, 3)
    try:
        posts_page = paginator.page(page)

        if page != 1:
            sleep(1.2)
    except PageNotAnInteger:
        posts_page = paginator.page(1)
    except EmptyPage:
        posts_page = paginator.page(paginator.num_pages)

    return render(request, "posts/posts.html",
                  {"posts": posts_page,
                   "pinned_posts": pinned_posts,
                   "top_posts": top_3_posts,
                   "filter_form": post_filter_form,
                   "club": club,
                   "club_slug": club_name_slug
                   })

@login_required
def post_detail(request, club_name_slug, encrypted_id):
    post = get_object_or_404(Post, encrypted_id=encrypted_id)

    return render(request, "posts/post_detail.html", {"post": post, "club_name_slug":club_name_slug})


def add_post(request, club_name_slug):
    if request.method == "POST":
        form = PostCreationForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            club_name = club_name_slug.replace('-', ' ')
            club = get_object_or_404(Club, name=club_name)
            post.author = request.user
            post.club = club
            post.save()
            return redirect("posts:posts", club_name_slug)
    else:
        form = PostCreationForm()
    context = {
        "form": form,
    }
    return render(request, "posts/post_add.html", context)

@login_required
def edit_post(request, club_name_slug, id):
    post = get_object_or_404(Post, id=id)
    if request.method == "POST":
        form = PostCreationForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect("posts:posts", club_name_slug)
    else:
        form = PostCreationForm(instance=post)
    context = {
        "form": form,
    }
    return render(request, "posts/post_edit.html", context)

@login_required
def post_update(request, club_name_slug, encrypted_id):
    if request.method == "GET":
        return HttpResponse("Incoming data could not be properly parsed. Try again later")

    post = get_object_or_404(Post, encrypted_id=encrypted_id)

    if post.author != request.user and (not ClubModerator.objects.filter(user=request.user, club=post.club).exists()):
        raise PermissionDenied("You are not allowed to issue updates for this post")

    puform = PostUpdateForm(request.POST)
    if puform.is_valid():

        p_update = puform.save(commit=False)
        p_update.post = post
        p_update.author = request.user
        p_update.save()
        return redirect('posts:post_detail', post.club.name.replace(' ', '-'), post.encrypted_id)
