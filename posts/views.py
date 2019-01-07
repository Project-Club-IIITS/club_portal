from time import sleep

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404

# Create your views here.
from base.models import Club
from posts.forms import PostFilterForm
from posts.models import PinnedPost, Post


def posts(request, club_name_slug):
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


def post_detail(request, club_name_slug, encrypted_id):
    post = get_object_or_404(Post, encrypted_id=encrypted_id)

    return render(request, "posts/post_detail.html", {"post": post})

