from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from .models import Category, Post
from django.core.paginator import Paginator, EmptyPage,\
                                  PageNotAnInteger


# Create your views here.
def post_list(request, category_slug=None):
    posts = Post.published.all()
    object_list = Post.published.all()
    paginator = Paginator(object_list, 4)  # 1 posts in each page
    page = request.GET.get('page')

    query = None
    category = None

    if request.GET:
        if 'category' in request.GET:
            categories = request.GET['category'].split(',')
            posts = posts.filter(category__name__in=categories)
            categories = Category.objects.filter(name__in=categories)

        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                messages.error(request, "You didn't enter any search query")
                return redirect(reverse('blog'))

            queries = Q(name__icontains=query) | Q(body__icontains=query) | Q(title__icontains=query )
            posts = posts.filter(queries)

 
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # if page is no an integer deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
        # If page is not of range deliver last page of result
        posts = paginator.page(paginator.num_pages)

    return render(request, 'blog/post/list.html', {'page': page,
                                                   'posts': posts,
                                                   'search_term': query,
                                                   'paginator': paginator})


def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post,
                                   status='published',
                                   publish__year=year,
                                   publish__month=month,
                                   publish__day=day)

    return render(request, 'blog/post/detail.html', {'post': post})