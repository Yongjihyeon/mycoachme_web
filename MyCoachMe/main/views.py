from django.shortcuts import render ,redirect, get_object_or_404
from .models import Post, Comment,AdminUser
from django.contrib.auth.models import User
from django.utils import timezone
from django.contrib import auth	

# Create your views here.
def home(request):
    posts= Post.objects.all()
    return render(request,'home.html',{'posts':posts})

def detail(request, post_id):
    post_detail = get_object_or_404(Post, pk=post_id)
    return render(request,'detail.html',{'post':post_detail})

def create(request):
    if request.method=="POST":
        post= Post()
        post.title = request.POST['title']
        post.body = request.POST['body']
        post.date = timezone.now()
        
        try:
            post.image = request.FILES['image']
        except:
            post.image = None
        post.save()
        
        return redirect('/detail/'+str(post.id),{'post':post})
    else:
        post = Post()
        return render(request,'create.html',{'post':post})
    
    
def update(request, post_id):
    post = Post.objects.get(id=post_id)
    if request.method == "POST":
        post.title = request.POST['title']
        post.body = request.POST['body']
        post.date = timezone.now()
        try:
            post.image = request.FILES['image']
        except:
            post.image = None
        post.save()
        return redirect('/detail/'+str(post.id),{'post':post})
    else:
        post=Post()
        return render(request, 'update.html', {'post':post})

def delete(request, post_id):
    post = Post.objects.get(id=post_id)
    post.delete()
    return redirect('home')

def detail(request,post_id):
    post_detail = get_object_or_404(Post,pk=post_id)
    comments = Comment.objects.filter(post = post_id)
    if request.method == "POST":
        comment = Comment()
        comment.post = post_detail
        comment.body = request.POST['body']
        comment.date = timezone.now()
        comment.save()
    return render(request,'detail.html',{'post':post_detail, 'comments':comments})


# def signup(request):
#     if request.method == 'POST':
#         if request.POST['password1'] == request.POST['password2']:
#             username = request.POST['username']
#             password = request.POST['password1']
#             user = User.objects.create_user(username=username, password=password)
#             user.save()  # 관리자에 사용자 등록
            
#             return redirect('login')  # 로그인 페이지로 리다이렉트
        
#     return render(request, 'signup.html')


def send_to_admin(data):
    try:
        admin_user = AdminUser.objects.create(
            username=data['username'],
            birth_year=data['birth_year'],
            height=data['height'],
            weight=data['weight'],
            exercise_area=data['exercise_area']
        )
        admin_user.save()
        print("User data saved to admin database successfully.")
    except Exception as e:
        print(f"Error saving user data to admin database: {str(e)}")


def signup(request):
    if request.method == 'POST':
        if request.POST['password1'] == request.POST['password2']:
            username = request.POST['username']

            # 사용자명(아이디)의 고유성 확인
            if User.objects.filter(username=username).exists():
                return render(request, 'signup.html', {'error': '이미 사용 중인 아이디입니다.'})

            password = request.POST['password1']
            birth_year = request.POST.get('birth_year', 2000)
            height = request.POST.get('height', 150)
            weight = request.POST.get('weight', 50)
            exercise_area = request.POST.get('exercise_area', '')

            user = User.objects.create_user(username=username, password=password)
            user.save()

            admin_data = {
                'username': username,
                'birth_year': birth_year,
                'height': height,
                'weight': weight,
                'exercise_area': exercise_area
            }
            send_to_admin(admin_data)

            return redirect('login')

    return render(request, 'signup.html')

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(request, username = username, password = password)
        if user is not None:
            auth.login(request, user)
            return redirect('home')
        else:
            return render(request, 'login.html', {'error' : 'username or password is incorrect.'})
    else:
    	return render(request, 'login.html')

def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        return redirect('home')
    return render(request, 'login.html')