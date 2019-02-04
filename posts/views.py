from time import sleep

from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.core.mail import send_mail
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db import IntegrityError
from django.db.models import F
from django.http import JsonResponse, HttpResponse, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.template.loader import render_to_string

from accounts.models import Calendar
from base.models import Club, ClubModerator, ClubMember
from base.utils import run_in_background
from base.views import send_new_post_notification, send_post_update_notification
from posts.models import PinnedPost, Post, Vote, Option, Poll, Event, PostApprover, News
from posts.forms import PostFilterForm, PostCreationForm, PostUpdateForm, EventForm, PollCreateForm


def redirect_with_args(url, GET_args=None, *args, **kwargs):
    response = redirect(url, *args, **kwargs)

    response['Location'] += '?'

    if GET_args:
        for key in GET_args:
            response['Location'] += str(key) + '=' + str(GET_args[key])

    return response


@login_required
def posts(request):
    following_clubs = request.user.userprofile.following_clubs.all()
    following_clubs_id = [club.id for club in following_clubs]

    posts = Post.objects.filter(is_approved=True, is_public=True, is_published=True).filter(
        club__id__in=following_clubs_id)
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

    posts = club.post_set.filter(club=club, is_approved=True, is_published=True)

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

    # print(posts)

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
def events(request):
    return redirect_with_args(url='posts:posts', GET_args={'events_only': True})


@login_required
def club_events(request, club_name_slug):
    return redirect_with_args(club_name_slug, url='posts:posts', GET_args={'events_only': True})


@login_required
def polls(request):
    return redirect_with_args(url='posts:posts', GET_args={'polls_only': True})


@login_required
def club_polls(request, club_name_slug):
    return redirect_with_args('posts:club_posts', {'polls_only': True}, club_name_slug)


@login_required
def post_detail(request, club_name_slug, encrypted_id):
    club_name = club_name_slug.replace('-', ' ')
    club = get_object_or_404(Club, name=club_name)
    post = get_object_or_404(Post, encrypted_id=encrypted_id)

    is_liked = request.user.liked_users.filter(id=post.id).exists()

    if (not post.is_public) and (not club.clubmember_set.filter(user=request.user).exists()):
        # Post is not public and User is not a club member
        raise PermissionDenied("You are not authorised to view this post")

    return render(request, "posts/post_detail.html", {"post": post,
                                                      "club_name_slug": club_name_slug,
                                                      "is_liked": is_liked
                                                      })


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
        send_post_update_notification(request, p_update)
        return redirect('posts:post_detail', post.club.name.replace(' ', '-'), post.encrypted_id)


@login_required
def cast_vote(request, club_name_slug, encrypted_id):
    if request.method != "POST":
        raise Http404("Only method POST is allowed")

    club_name = club_name_slug.replace('-', ' ')
    club = get_object_or_404(Club, name=club_name)
    post = get_object_or_404(Post, encrypted_id=encrypted_id)
    if not hasattr(post, 'poll'):
        raise Http404('This post is not a poll')

    poll = post.poll

    if not poll.is_active:
        raise HttpResponse("The poll has ended")

    if Vote.objects.filter(poll=poll, user=request.user).exists():
        raise PermissionDenied("You can vote only once")

    if not poll.post.is_public:
        # Make sure user is a member of the club
        if not club.clubmember_set.filter(user=request.user, is_approved=True).exists():
            raise PermissionDenied("You are not a part of this club. You can not vote")

    submitted_option = int(request.POST['option'])

    option = get_object_or_404(Option, id=submitted_option)

    v = Vote(poll=poll, user=request.user)

    option.num_votes = F('num_votes') + 1
    # This is done to avoid race condition where 2 users may try to update db at the same time
    # https://docs.djangoproject.com/en/2.1/ref/models/expressions/#avoiding-race-conditions-using-f

    option.save()

    if poll.track_votes:
        # Track the option user has voted for
        v.option = option

    v.save()

    response = redirect('posts:post_detail', club_name_slug, encrypted_id)

    response['location'] += '#results'

    return response


@login_required()
def likePost(request, id):
    post = get_object_or_404(Post, id=id)

    if request.method == 'POST':

        is_liked = post.liked_users.filter(id=request.user.id).exists()
        print(is_liked)

        if (is_liked):
            post.liked_users.remove(request.user)
            post.reclac_likes()
            is_liked = False
        else:
            post.liked_users.add(request.user)
            post.reclac_likes()
            is_liked = True

        post.save()

        data = {
            'is_liked': is_liked
        }

        return JsonResponse(data)


def create_post_generic(request, club, post_create_form):
    post = post_create_form.save(commit=False)
    post.author = request.user
    post.club = club
    post.save()

    if ClubModerator.objects.filter(club=club, user=request.user).exists():
        PostApprover.objects.create(post=post, user=request.user)
        post.is_approved = True
        post.save()

    if post.club.name in ["clubs_portal", "Campus Life Committee"]:
        News.objects.create(message=post.title, post=post)

    post.subscribed_users.add(request.user)
    return post


@login_required
def create_post(request, club_name_slug):
    club_name = club_name_slug.replace('-', ' ')
    club = get_object_or_404(Club, name=club_name)

    if not ClubMember.objects.filter(club=club, user=request.user).exists():
        raise PermissionDenied("Only Club members can create posts")

    if request.method == "POST":
        form = PostCreationForm(request.POST, request.FILES)
        if form.is_valid():
            post = create_post_generic(request, club, form)
            if post.is_approved:
                send_new_post_notification(request, post)
            return redirect("posts:post_detail", club_name_slug, post.encrypted_id)

    else:
        form = PostCreationForm()

    context = {
        "form": form,
    }
    return render(request, "posts/post_add.html", context)


@login_required
def edit_post(request, encrypted_id):
    post = get_object_or_404(Post, encrypted_id=encrypted_id)
    if post.author != request.user:
        raise PermissionDenied("You are not authorized to edit this post")

    if request.method == "POST":
        form = PostCreationForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            club_name_slug = post.club.name.replace(' ', '-')
            return redirect("posts:post_detail", club_name_slug, post.encrypted_id)
    else:
        form = PostCreationForm(instance=post)
    context = {
        "form": form,
    }
    return render(request, "posts/post_edit.html", context)


@login_required
def create_poll(request, club_name_slug):
    club_name = club_name_slug.replace('-', ' ')
    club = get_object_or_404(Club, name=club_name)

    if not ClubMember.objects.filter(club=club, user=request.user).exists():
        raise PermissionDenied("Only Club members can create posts")

    if request.method == "POST":
        print(request.POST)
        post_create_form = PostCreationForm(request.POST, request.FILES)
        poll_create_form = PollCreateForm(request.POST)

        if post_create_form.is_valid() and poll_create_form.is_valid():
            post = create_post_generic(request, club, post_create_form)

            if 'cover_image' in request.FILES:
                post.cover_image = request.FILES['cover_image']
                post.save()
            poll = poll_create_form.save(commit=False)
            poll.post = post
            poll.save()

            option_count = int(request.POST['hidden-count'])
            for option in range(option_count):
                Option.objects.create(poll=poll, option_text=request.POST[str(option)])

            if post.is_approved:
                send_new_post_notification(request, post)

            return redirect('posts:post_detail', club_name_slug, post.encrypted_id)
    else:
        post_create_form = PostCreationForm()
        poll_create_form = PollCreateForm()

    return render(request, 'posts/poll_create.html', {'club_name': club_name_slug,
                                                      "post_create_form": post_create_form,
                                                      "poll_create_form": poll_create_form
                                                      }
                  )


@login_required
def edit_poll(request, encrypted_id):
    poll = get_object_or_404(Poll, post__encrypted_id=encrypted_id)
    if poll.post.author != request.user:
        raise PermissionDenied("You are not authorized to edit this post")

    if request.method == "POST":
        post_form = PostCreationForm(request.POST, request.FILES, instance=poll.post)
        poll_form = PollCreateForm(request.POST, instance=poll)

        if post_form.is_valid() and poll_form.is_valid():
            poll_form.save()
            post_form.save()

            return redirect('posts:post_detail', poll.post.club.name.replace(' ', '-'), poll.post.encrypted_id )

    else:
        post_form = PostCreationForm(instance=poll.post)
        poll_form = PollCreateForm(instance=poll)


    return render(request, 'posts/poll_create.html', {'club_name': poll.post.club.name.replace(' ', '-'),
                                                      "post_create_form": post_form,
                                                      "poll_create_form": poll_form,
                                                      "edit": True
                                                      }
                  )


# @login_required
# def edit_poll(request, encrypted_id):
#     post = get_object_or_404(Post, encrypted_id=encrypted_id)
#     if post.author != request.user:
#         raise PermissionDenied("You are not authorized to edit this post")
#
#     if request.method == "POST":
#         form = PostCreationForm(request.POST, request.FILES, instance=post)
#         if form.is_valid():
#             form.save()
#             club_name_slug = post.club.name.replace(' ', '-')
#             return redirect("posts:post_detail", club_name_slug, post.encrypted_id)
#     else:
#         form = PostCreationForm(instance=post)
#     context = {
#         "form": form,
#     }
#     return render(request, "posts/post_edit.html", context)


@login_required
def events_create(request, club_name_slug):
    club_name = club_name_slug.replace('-', ' ')
    club = get_object_or_404(Club, name=club_name)
    user = request.user
    if not ClubMember.objects.filter(club=club, user=request.user).exists():
        raise PermissionDenied("Only Club members can create posts")
    if request.method == "POST":
        postform = PostCreationForm(request.POST, request.FILES)
        eventform = EventForm(data=request.POST)
        if postform.is_valid() and eventform.is_valid():
            post = create_post_generic(request, club, postform)
            event = eventform.save(commit=False)
            event.post = post
            event.save()

            if post.is_approved:
                send_new_post_notification(request, post)

            return redirect('posts:post_detail', club_name_slug, post.encrypted_id)


    else:
        postform = PostCreationForm()
        eventform = EventForm()

    return render(request, 'posts/event_create.html', {'postform': postform, 'eventform': eventform})


@login_required
def events_edit(request, encrypted_id):
    post = get_object_or_404(Post, encrypted_id=encrypted_id)
    event = get_object_or_404(Event, post=post)
    if request.user != post.author:
        raise PermissionDenied("You are not allowed to edit this event")

    if request.method == "POST":
        eventform = EventForm(request.POST or None, instance=event)
        postform = PostCreationForm(request.POST, request.FILES, instance=post)
        if postform.is_valid() and eventform.is_valid():
            postform.save()
            eventform.save()

            return redirect('posts:post_detail', post.club.name.replace(' ', '-'), post.encrypted_id)

    else:
        eventform = EventForm(instance=event)
        postform = PostCreationForm(instance=post)
    return render(request, 'posts/event_create.html', {'postform': postform, 'eventform': eventform})


@login_required
def interested_event(request):
    ret_data = {
        'add_success': False
    }
    if not request.user.is_authenticated:
        return JsonResponse(ret_data)
    user = request.user
    encrypted_id = request.POST.get('encrypted_id')
    post = get_object_or_404(Post, encrypted_id=encrypted_id)
    event = get_object_or_404(Event, post=post)
    if user not in event.interested_users.all():
        event.interested_users.add(user)
        event.save()
        ret_data['add_success'] = True

    Calendar.objects.create(date=event.start_date.date(), work_title=event.post.title, user=user)

    return JsonResponse(ret_data)


@login_required
def subscribe(request, club_name_slug, encrypted_id):
    club_name = club_name_slug.replace('-', ' ')
    club = get_object_or_404(Club, name=club_name)
    post = get_object_or_404(Post, encrypted_id=encrypted_id, club=club)

    post.subscribed_users.add(request.user)


    return redirect('posts:post_detail', club_name_slug, encrypted_id)


@login_required
def unsubscribe(request, club_name_slug, encrypted_id):
    club_name = club_name_slug.replace('-', ' ')
    club = get_object_or_404(Club, name=club_name)
    post = get_object_or_404(Post, encrypted_id=encrypted_id, club=club)

    post.subscribed_users.remove(request.user)

    return redirect('posts:post_detail', club_name_slug, encrypted_id)


@login_required
def event_interested(request, club_name_slug, encrypted_id):
    club_name = club_name_slug.replace('-', ' ')
    club = get_object_or_404(Club, name=club_name)
    post = get_object_or_404(Post, encrypted_id=encrypted_id, club=club)

    if hasattr(post, 'event'):
        post.event.interested_users.add(request.user)

    post.subscribed_users.add(request.user)

    Calendar.objects.create(date=post.event.start_date.date(), work_title=post.event.post.title, user=request.user)

    return redirect('posts:post_detail', club_name_slug, encrypted_id)


@login_required
def event_uninterested(request, club_name_slug, encrypted_id):
    club_name = club_name_slug.replace('-', ' ')
    club = get_object_or_404(Club, name=club_name)
    post = get_object_or_404(Post, encrypted_id=encrypted_id, club=club)

    if hasattr(post, 'event'):
        post.event.interested_users.remove(request.user)

    post.subscribed_users.remove(request.user)

    return redirect('posts:post_detail', club_name_slug, encrypted_id)


@login_required
def pin_post(request, club_name_slug, encrypted_id):
    club_name = club_name_slug.replace('-', ' ')
    club = get_object_or_404(Club, name=club_name)
    post = get_object_or_404(Post, encrypted_id=encrypted_id, club=club)

    if ClubModerator.objects.filter(user=request.user, club=club).exists():
        try:
            PinnedPost.objects.create(post=post)
        except IntegrityError:
            pass

    return redirect('posts:post_detail', club_name_slug, encrypted_id)


@login_required
def unpin_post(request, club_name_slug, encrypted_id):
    club_name = club_name_slug.replace('-', ' ')
    club = get_object_or_404(Club, name=club_name)
    post = get_object_or_404(Post, encrypted_id=encrypted_id, club=club)

    if ClubModerator.objects.filter(user=request.user, club=club).exists():
        try:
            PinnedPost.objects.filter(post=post).delete()
        except:
            pass

    return redirect('posts:post_detail', club_name_slug, encrypted_id)
