from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from .forms import PostForm
from .models import Post, Reaction
from .services import rank_feed


def feed(request):
    posts = rank_feed()[:50]
    form = PostForm() if request.user.is_authenticated else None
    return render(request, "community/feed.html", {"posts": posts, "form": form})


@login_required
def create_post(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            # New posts start unapproved and enter the moderation queue —
            # see docs/02-core-platform-systems.md, "Moderation System".
            post.is_approved = False
            post.save()
            messages.success(request, "Posted — it'll appear in the feed once reviewed.")
    return redirect("community:feed")


@login_required
def react(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    reaction_type = request.POST.get("reaction_type", "inspiration")
    Reaction.objects.get_or_create(post=post, user=request.user, defaults={"reaction_type": reaction_type})
    return redirect("community:feed")
