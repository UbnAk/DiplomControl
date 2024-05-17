from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Comment
from .forms import PostForm, CommentForm,CustomUserCreationForm, PostReactionForm
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import Post, PostReaction


def post_list(request):
    posts = Post.objects.all()  # Получаем все объекты Post

    # Печать объектов posts для отладки
    for post in posts:
        print(f"Пост: {post.title}, Автор: {post.author.username}, Дата: {post.created_at}")

    try:
        # Рендеринг шаблона с объектами posts
        return render(request, 'myapp/post_list.html', {'posts': posts})
    except Exception as e:
        # Обработка исключения при рендеринге шаблона
        print(f"Ошибка при рендеринге шаблона post_list.html: {e}")
        # Здесь вы можете добавить дополнительную обработку исключения или логирование
        return render(request, 'myapp/error.html', {'error_message': str(e)})
    



def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments = post.comments.all()
    reactions = post.reactions.all()
    reaction_form = PostReactionForm(request.POST or None)

    if request.method == 'POST':
        print(f"Форма реакции: {reaction_form.data}")  # Дополнительный вывод данных формы
        if reaction_form.is_valid():
            print("Форма реакции валидна")  # Дополнительный вывод
            reaction = reaction_form.save(commit=False)
            reaction.post = post
            reaction.user = request.user
            reaction.save()
            reaction_form = PostReactionForm()  # Reset the form
        else:
            print(f"Форма реакции не валидна: {reaction_form.errors}")
    post = get_object_or_404(Post, pk=pk)
    comments = post.comments.all()
    reactions = post.reactions.all()
    reaction_form = PostReactionForm(request.POST or None)

    if request.method == 'POST':
        if reaction_form.is_valid():
            reaction = reaction_form.save(commit=False)
            reaction.post = post
            reaction.user = request.user
            reaction.save()
            reaction_form = PostReactionForm()  # Reset the form

    context = {
        'post': post,
        'comments': comments,
        'reactions': reactions,
        'reaction_form': reaction_form,
    }
    return render(request, 'myapp/post_detail.html', context)


@login_required
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'myapp/post_edit.html', {'form': form})

# @login_required
# def post_edit(request, pk):
#     post = get_object_or_404(Post, pk=pk)
#     if request.method == "POST":
#         form = PostForm(request.POST, instance=post)
#         if form.is_valid():
#             post = form.save(commit=False)
#             post.author = request.user
#             post.save()
#             return redirect('post_detail', pk=post.pk)
#     else:
#         form = PostForm(instance=post)
#     return render(request, 'myapp/post_edit.html', {'form': form})

@login_required
def add_comment(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'myapp/add_comment.html', {'form': form})


@login_required
def post_reaction(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    
    if request.method == 'POST':
        reaction_type = request.POST.get('reaction_type')
        if reaction_type == 'like':
            reaction, created = PostReaction.objects.update_or_create(
                post=post,
                user=request.user,
                defaults={'reaction': 'like'}
            )
        elif reaction_type == 'dislike':
            reaction, created = PostReaction.objects.update_or_create(
                post=post,
                user=request.user,
                defaults={'reaction': 'dislike'}
            )
        else:
            return JsonResponse({'error': 'Invalid reaction type'}, status=400)
        
        # Перенаправить на ту же страницу после обработки реакции
        return redirect('post_detail', pk=post.pk)

    # Получить данные для отображения на странице
    reactions = PostReaction.objects.filter(post=post)
    comments = post.comments.all()
    comment_form = CommentForm()

    context = {
        'post': post,
        'reactions': reactions,
        'comments': comments,
        'comment_form': comment_form,
    }
    return render(request, 'myapp/post_detail.html', context)

@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.user != post.author:
        return redirect('post_detail', pk=post.pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'myapp/post_edit.html', {'form': form})

@login_required
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.user != post.author:
        return redirect('post_detail', pk=post.pk)
    post.delete()
    return redirect('post_list')

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'myapp/register.html', {'form': form})


@login_required
def comment_delete(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    if comment.author != request.user:
        # Не разрешать удаление комментариев, написанных другими пользователями
        return redirect('post_detail', pk=comment.post.pk)
    if request.method == 'POST':
        comment.delete()
        return redirect('post_detail', pk=comment.post.pk)
    return render(request, 'myapp/comment_delete.html', {'comment': comment})