from time import sleep

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404

# Create your views here.
from base.models import Club
from posts.forms import PostFilterForm, EventForm, PostForm
from posts.models import PinnedPost, Post, Event


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
    # adwait rox
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


def events_create(request, club_name_slug):
    club_name = club_name_slug.replace('-', ' ')
    club = get_object_or_404(Club, name=club_name)
    user = request.user

    if request.method == "POST":
        postform = PostForm(data=request.POST)
        eventform = EventForm(data=request.POST)
        if postform.is_valid() and eventform.is_valid():
            post = postform.save(commit=False)
            post.author = user
            post.club = club
            # postform.encrypted_id=
            post = post.save()
            event = eventform.save(commit=False)
            event.post = post
            event.save()

            return redirect(request, '')


    else:
        postform = PostForm()
        eventform = EventForm()

    return render(request, 'posts/event_create.html', {'postform': postform, 'eventform': eventform})


def events_update(request, club_name_slug, encrypted_id):
    post = get_object_or_404(Post, encrypted_id=encrypted_id)
    event = get_object_or_404(Event, post=post)
    club_name = club_name_slug.replace('-', ' ')
    if event.post.club is club_name:
        eventform = EventForm(request.POST or None, instance=event)
        postform = PostForm(request.POST or None, instance=post)
        if request.method == 'POST':
            if postform.is_valid() and eventform.is_valid():
                postform.save()
                eventform.save()

                return render(request, '')

        else:
            return render(request, 'posts/event_update.html', {'postform': postform, 'eventform': eventform})


def interested_event(request):
    ret_data = {
        'add_success': False
    }
    if request.user.is_annonymous:
        return JsonResponse(ret_data)
    user = request.user
    encrypted_id = request.POST.get('encrypted_id')
    post = get_object_or_404(Post, encrypted_id=encrypted_id)
    event = get_object_or_404(Event, post=post)
    if not event.interested_users.filter(user=user).exists():
        event.interested_users.add(user)
        event.save()
        ret_data['add_success'] = True

    return JsonResponse(ret_data)
