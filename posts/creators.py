from .models import Post
from django.contrib.auth.models import User
import random
from base.models import Club


def create_posts(count):
    users = User.objects.all()
    clubs = Club.objects.all()

    cur_count = Post.objects.all().count()
    for i in range(count):
        Post.objects.create(author=users[random.randint(0, len(users) - 1)],
                            club=clubs[random.randint(0, len(clubs)-1)],
                            is_approved=True,
                            title = f"Sample Post #{cur_count+i}",
                            body = "This is a sample Post",
                            is_public=True,
                            )
