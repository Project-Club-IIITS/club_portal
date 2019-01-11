from time import sleep

from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.
from base.models import Club, ClubModerator, ClubMember
from posts.forms import PostFilterForm, PostCreationForm, PostUpdateForm
from posts.models import PinnedPost, Post


@login_required
def posts(request):
    following_clubs = request.user.userprofile.following_clubs.all()
    following_clubs_id = [club.id for club in following_clubs]

    posts = Post.objects.filter(is_approved=True, is_public=True).filter(club__id__in=following_clubs_id)
    post_filter_form = PostFilterForm(request.GET)

    posts = post_filter_form.filter_posts(posts)

    #
    # memberclubs = ClubMember.objects.all().exclude(user=request.user, is_approved=True)
    # print(memberclubs)
    # # List of clubmember objects in which user is NOT a member
    # clubs = [m.club for m in memberclubs]
    #
    # # First Exclude all posts which are not public
    # public_posts = posts.exclude(is_public=False)
    #
    # # Get all posts which are not public but user is member of that club
    # member_posts = posts.filter(is_public=False, club__in=clubs)
    #
    # # Get a union of public_posts and member_posts
    # posts = public_posts | member_posts
    #

    page = 1
    if 'page' in post_filter_form.cleaned_data:
        if post_filter_form.cleaned_data['page']:
            page = post_filter_form.cleaned_data['page']

    paginator = Paginator(posts, 10)
    try:
        posts_page = paginator.page(page)

        if page != 1:
            sleep(1.2)
    except PageNotAnInteger:
        posts_page = paginator.page(1)
    except EmptyPage:
        posts_page = paginator.page(paginator.num_pages)

    context = {"posts": posts_page,
               "filter_form": post_filter_form,
               }

    if page == 1:
        # This is done to reduce unnecesary db queries if page is greater than 1
        # First page, take pinned posts and top posts
        top_3_posts = posts.order_by('-votes')[:3]

        pinned_posts = PinnedPost.objects.filter(post__is_public=True)

        context["top_posts"] = top_3_posts
        context["pinned_posts"] = pinned_posts

    return render(request, "posts/general_post.html", context)


@login_required
def club_posts(request, club_name_slug):
    club_name = club_name_slug.replace('-', ' ')
    club = get_object_or_404(Club, name=club_name)

    posts = club.post_set.filter(club=club, is_approved=True)

    is_member = True
    if not ClubMember.objects.filter(club=club, user=request.user, is_approved=True).exists():
        is_member = False
        posts = posts.filter(is_public=True)
        # User is not a club member. Only show posts which are public

    top_3_posts = posts.order_by('-votes')[:3]

    pinned_posts = PinnedPost.objects.filter(post__club=club)

    post_filter_form = PostFilterForm(request.GET)

    posts = post_filter_form.filter_posts(posts)
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

    context = {"posts": posts_page,
               "filter_form": post_filter_form,
               "club": club,
               "club_slug": club_name_slug
               }

    if page == 1:
        # This is done to reduce unnecesary db queries if page is greater than 1
        # First page, take pinned posts and top posts
        top_3_posts = posts.order_by('-votes')[:3]

        pinned_posts = PinnedPost.objects.filter(post__club=club)

        if not is_member:
            pinned_posts = pinned_posts.filter(post__is_public=True)

        context["top_posts"] = top_3_posts
        context["pinned_posts"] = pinned_posts

    return render(request, "posts/posts.html", context)


@login_required
def post_detail(request, club_name_slug, encrypted_id):
    club_name = club_name_slug.replace('-', ' ')
    club = get_object_or_404(Club, name=club_name)
    post = get_object_or_404(Post, encrypted_id=encrypted_id)

    if (not post.is_public) and (not club.clubmember_set.filter(user=request.user).exists()):
        # Post is not public and User is not a club member
        raise PermissionDenied("You are not authorised to view this post")

    return render(request, "posts/post_detail.html", {"post": post, "club_name_slug": club_name_slug})


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
