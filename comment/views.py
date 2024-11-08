from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from .models import Comment
from .forms import CommentForm


def home(request):
    """
    Renders the home page with a list of top-level comments (those without a parent).
    Supports sorting by creation date (default), username, or email. The comments are
    paginated, with 25 comments displayed per page.

    Sorting options:
        - 'LIFO': Sorts by creation date, with the most recent comments first (default).
        - 'name': Sorts by the username of the comment authors in ascending order.
        - 'email': Sorts by the email of the comment authors in ascending order.

    The home page provides navigation for multiple pages of comments and the option to
    choose a sorting method through query parameters.

    :param request: The HTTP request object that contains query parameters for sorting and pagination.
    :return: Rendered 'index.html' template with paginated and optionally sorted comments.
    """
    sort_option = request.GET.get('sort', 'LIFO')

    if sort_option == 'name':
        comments = Comment.objects.filter(parent=None).order_by('user__username')
    elif sort_option == 'email':
        comments = Comment.objects.filter(parent=None).order_by('email')
    else:
        comments = Comment.objects.filter(parent=None).order_by('-created_at')

    paginator = Paginator(comments, 25)
    page_number = request.GET.get('page')
    try:
        comments = paginator.page(page_number)
    except PageNotAnInteger:
        comments = paginator.page(1)
    except EmptyPage:
        comments = paginator.page(paginator.num_pages)

    return render(request, 'index.html', {'comments': comments, 'sort_option': sort_option})


# @login_required(login_url='login')
def add_comment(request, parent_id=None):
    """
    Handles submission of a new comment or reply. If the form is valid, it saves the comment,
    broadcasts it to all connected WebSocket clients, and redirects to the home page.
    Optionally validates a CAPTCHA if included in the form.

    If a `parent_id` is provided, the comment is treated as a reply to the specified parent comment.

    If the CAPTCHA validation fails, an error message is displayed and the form is re-rendered.

    :param request: The HTTP request object containing the POST data for submitting the comment.
    :param parent_id: The ID of the parent comment, if replying to an existing comment (optional).
    :return: Redirect to the home page upon successful submission or render the form again on failure.
    """
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            if parent_id:
                parent_comment = get_object_or_404(Comment, id=parent_id)
                form.instance.parent = parent_comment
            form.save()
            return redirect('index')
    else:
        form = CommentForm()

    return render(request, 'comment.html', {'form': form, 'parent_id': parent_id})


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})




