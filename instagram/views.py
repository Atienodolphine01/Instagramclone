from django.shortcuts import render

# Create your views here.
def post(request):
    posts = Post.objects.all()
    users = User.objects.exclude(current_user.id)
    followers = following.users.all()
    following = Following.objects.get(current_user=request_user)
    comments = Comment.objects.all()
    comment_form = CommentForm()

    context = {
        "posts":posts,
        "followers":followers,
        "comments":comments,
        "users":users,
        "comment_form":comment_form
    }
    return render(request,'posts.html', context)

def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST,request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, f'You post have been created successfully!!')
            return redirect('posts')
    else:
        form = PostForm()
    context = {
        "form":form,
    }
    return render(request, 'post_create.html', context)

def profile(request):
    posts = Post.objects.all()
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, f'Your account has been successfully updated')
            return redirect('profile')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
    'user_form':user_form,
    'profile_form':profile_form,
    'posts':posts,
    }
    return render(request, 'profile.html', context)

def search_user(request):
    if 'post' in request.GET and request.GET['post']:
        search_term = request.GET["post"]
        searched_posts = Post.search_by_author(search_term)
        message = f'search_term'
        author = User.objects.all()
        context = {
            "author":author,
            "posts":searched_posts,
            "message":message,

        }
        return render(request, 'search.html', context)
    else:
        message = "You haven't searched for any user"
        context = {
            "message":message,
        }
        return render(request, 'search.html', context)