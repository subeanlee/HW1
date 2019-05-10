from django.shortcuts import render, get_object_or_404, redirect
from .models import Blog
from django.utils import timezone
from .forms import CommentForm

# Create your views here.

def home(request):
    blogs = Blog.objects
    return render(request, 'home.html', {'blogs': blogs})

def detail(request, blog_id):
    blog_detail = get_object_or_404(Blog, pk= blog_id)
    return render(request, 'detail.html', {'blog': blog_detail})

def new(request):
    return render(request, 'new.html')

def create(request):
    blog = Blog()
    #블로그라는 클래스로 부터 'blog'객체 생성 / 객체 안에 title, body, pub_date 변수 존재
    blog.title = request.GET['title']
    # new.html에서 'title'이라고 하는 form에 입력한 내용을 여기로 가져와서 
    # blog라는 객체에 title변수에 담아주기
    blog.body = request.GET['body']
    blog.pub_date = timezone.datetime.now()
    # blog를 작성한 시점을 넣어주는 함수
    blog.save()
    # blog라는 객체에 넣어줬던 내용들을 데이터 베이스에 저장해라. (쿼리셋 메쏘드)
    return redirect('/blog/' + str(blog.id))
    # 해당 url로 넘기기

def delete(request, blog_id):
    blog = Blog.objects.get(pk= blog_id)
    blog.delete()
    return redirect('home')
    
def edit(request, blog_id):
    blog_edit = Blog.objects.get(pk= blog_id)
    return render(request, 'edit.html', {'blog': blog_edit})

def update(request, blog_id):
    blog = Blog.objects.get(pk= blog_id)
    blog.title = request.POST['title']
    blog.body = request.POST['body']
    blog.pub_date = timezone.datetime.now()
    blog.save()
    return redirect('home')

def comment_new(request, blog_id):
    post = get_object_or_404(Blog, pk=blog_id)
    if request.method == 'POST':
        form = CommentForm(reuqest.POST)
        if form.is_vaild():
            comment = form.save(commit=False)
            comment.post = Blog.objects.get(pk=blog_id)
            comment.save()
            return redirect('detail', blog_id)
    else:
        form = CommentForm()
    return render(request, 'blog_form.html', {'form':form,})
