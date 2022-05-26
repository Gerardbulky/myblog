from django.shortcuts import render, get_object_or_404
from django.core.mail import send_mail
from django.core.mail import send_mail
from .models import News
from .forms import EmailPostForm


def news_list(request):
    news = News.published.all()
    return render(request, 'letter/news/list.html', {'news': news})


def news_detail(request, year, month, day, news):
    news = get_object_or_404(News, slug=news,
                                   status='published',
                                   publish__year=year,
                                   publish__month=month,
                                   publish__day=day)
    return render(request,
                  'letter/news/details.html',
                  {'news': news})



def news_share(request, news_id):
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

