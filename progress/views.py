from django.views.generic.simple import direct_to_template
from posts import get_posts
from commits import get_commits

def progress(request):
    commits = get_commits()
    posts = get_posts()
    return direct_to_template(request, 'progress/progress.html', {"posts":posts, "commits":commits})
