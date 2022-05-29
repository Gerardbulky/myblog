from django.shortcuts import render, get_object_or_404
from django.core.mail import send_mail
from django.core.mail import send_mail
from .models import News, Comment
from .forms import EmailPostForm, CommentForm


def news_list(request):
    news = News.published.all()
    return render(request, 'letter/news/list.html', {'news': news})


def news_detail(request, year, month, day, news):
    news = get_object_or_404(News, slug=news,
                                   status='published',
                                   publish__year=year,
                                   publish__month=month,
                                   publish__day=day)
    # List of active comments for this post
    comments = news.comments.filter(active=True)
    new_comment = None
    if request.method == 'POST':
        # A comment was posted
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            # Create Comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
            # Assign the current post to the comment
            new_comment.news = news
            # Save the comment to the database
            new_comment.save()
    else:
        comment_form = CommentForm()

    return render(request,
                  'letter/news/details.html',
                  {'news': news,
                   'comments': comments,
                   'new_comment': new_comment,
                   'comment_form': comment_form})



def news_share(request, news_id): #passed in a new id for this particular possed news_id
    # Retrieve post by id
    news = get_object_or_404(News, id=news_id, status='published')
    sent = False
    if request.method == 'POST':
        # Form was submitted
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # Form fields passed validation
            cd = form.cleaned_data
            # ... send email
            news_url = request.build_absolute_uri(
                news.get_absolute_url())
            subject = f"{cd['name']} recommends you read " \
                      f"{news.title}"
            message = f"Read {news.title} at {news_url}\n\n" \
                      f"{cd['name']}\'s comments: {cd['comments']}"
            send_mail(subject, message, 'gerardbulky@gmail.com', [cd['to']])
            sent = True
    else:
        form = EmailPostForm()
    return render(request, 'letter/news/share.html', {'news': news,
                                                      'form': form,
                                                      'sent': sent})

