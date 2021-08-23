from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse

from mainapp.forms import SupportForm, CreateSupportForm, ChangeForm, ChangePassword, NewsForm, SupportFormAdmin, \
    ChangeFormAdmin, RegisterFormAdmin
from mainapp.models import News, Tickets


@login_required
def index(request):
    news = News.objects.all()
    context = {
        'title': 'главная',
        'news': news,
    }
    return render(request, 'mainapp/index.html', context)


@login_required
def my_ticket(request):
    ticket = Tickets.objects.filter(user_id=request.user.id)
    context = {
        'title': 'мои тикеты',
        'ticket': ticket,
    }
    return render(request, 'mainapp/tickets/my_ticket.html', context)


@login_required
def open_ticket(request, pk):
    ticket = Tickets.objects.filter(id=pk)
    context = {
        'title': f'Обращение: {request.user.first_name} | {request.user.username}',
        'ticket': ticket,
    }
    return render(request, 'mainapp/tickets/open_ticket.html', context)


@login_required
def create_ticket(request):
    if request.method == 'POST':
        form = CreateSupportForm(request.POST)
        if form.is_valid():
            support_form = form.save(commit=False)
            support_form.user = request.user
            support_form.save()
            messages.success(request, 'Вы успешно создали тикет!')
            return HttpResponseRedirect(reverse('mainapp:my_ticket'))
    else:
        form = CreateSupportForm()
    context = {
        'title': 'Создать обращение в тех.поддержку',
        'form': form,
    }
    return render(request, 'mainapp/tickets/create_ticket.html', context)


@login_required
def send_message(request, pk):
    ticket_get = get_object_or_404(Tickets, id=pk)
    if request.method == 'POST':
        form = SupportForm(request.POST, instance=ticket_get)
        if form.is_valid():
            ticket_get.send_ticket()
            form.save()
            messages.success(request, 'Вы успешно изменили тикет!')
            return redirect('mainapp:open_ticket', pk)
    else:
        form = SupportForm(instance=ticket_get)
    context = {
        'title': f'Ответить на обращение {request.user.username}',
        'form': form,
    }
    return render(request, 'mainapp/tickets/send_ticket.html', context)


@login_required
def close_ticket(request, pk):
    ticket_get = get_object_or_404(Tickets, id=pk)
    ticket_get.close_ticket()
    messages.success(request, 'Вы успешно закрыли тикет!')
    return redirect('mainapp:open_ticket', pk)


@login_required
def profile(request):
    context = {
        'title': 'профиль',
    }
    return render(request, 'mainapp/profile/index.html', context)


@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = ChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Вы успешно изменили профиль!')
            return HttpResponseRedirect(reverse('mainapp:edit_profile'))
    else:
        form = ChangeForm(instance=request.user)
    context = {
        'title': 'изменить профиль',
        'form': form,
    }
    return render(request, 'mainapp/profile/edit_profile.html', context)


@login_required
def change_password(request):
    if request.method == 'POST':
        form = ChangePassword(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, 'Вы успешно изменили пароль!')
            return HttpResponseRedirect(reverse('mainapp:change_password'))
    else:
        form = ChangePassword(user=request.user)
    context = {
        'title': 'изменить пароль',
        'form': form,
    }
    return render(request, 'mainapp/profile/change_password.html', context)


@login_required
def news(request):
    if request.user.is_superuser:
        news_list = News.objects.all()
        context = {
            'title': 'Новости',
            'news': news_list,
        }
        return render(request, 'adminapp/news/index.html', context)
    else:
        return HttpResponseRedirect(reverse('mainapp:index'))


@login_required
def create_news(request):
    if request.user.is_superuser:
        if request.method == 'POST':
            form = NewsForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Вы успешно создали новость!')
                return HttpResponseRedirect(reverse('mainapp:news'))
        else:
            form = NewsForm()
        context = {
            'title': 'Создать новость',
            'form': form,
        }
        return render(request, 'adminapp/news/create_news.html', context)
    else:
        return HttpResponseRedirect(reverse('mainapp:index'))


@login_required
def edit_news(request, pk):
    if request.user.is_superuser:
        news = get_object_or_404(News, id=pk)
        if request.method == 'POST':
            form = NewsForm(request.POST, instance=news)
            if form.is_valid():
                form.save()
                messages.success(request, 'Вы успешно изменили новость!')
                return HttpResponseRedirect(reverse('mainapp:news'))
        else:
            form = NewsForm(instance=news)
        context = {
            'title': 'изменить новость',
            'form': form,
        }
        return render(request, 'mainapp/tickets/create_ticket.html', context)
    else:
        return HttpResponseRedirect(reverse('mainapp:index'))


@login_required
def remove_news(request, pk):
    if request.user.is_superuser:
        news = get_object_or_404(News, id=pk)
        news.delete()
        messages.success(request, 'Вы успешно удалили новость!')
        return HttpResponseRedirect(reverse('mainapp:news'))
    else:
        return HttpResponseRedirect(reverse('mainapp:index'))


@login_required
def ticket_admin(request):
    if request.user.is_superuser or request.user.is_staff:
        if 'search_title' in request.GET:
            search_title = request.GET['search_title']
            ticket = Tickets.objects.filter(title__icontains=search_title)
            if not ticket:
                ticket = Tickets.objects.filter(user__username__icontains=search_title)
        else:
            ticket = Tickets.objects.all()
        context = {
            'title': 'все тикеты',
            'ticket': ticket,
        }
        return render(request, 'adminapp/tickets/index.html', context)
    else:
        return HttpResponseRedirect(reverse('mainapp:index'))


@login_required
def open_ticket_admin(request, pk):
    if request.user.is_superuser or request.user.is_staff:
        ticket = Tickets.objects.filter(id=pk)
        context = {
            'title': f'Обращение',
            'ticket': ticket,
        }
        return render(request, 'adminapp/tickets/open_ticket.html', context)
    else:
        return HttpResponseRedirect(reverse('mainapp:index'))


@login_required
def open_ticket_message(request, pk):
    if request.user.is_superuser or request.user.is_staff:
        ticket = get_object_or_404(Tickets, id=pk)
        ticket.send_ticket()
        return redirect('mainapp:open_ticket_admin', pk)

@login_required
def send_message_admin(request, pk):
    if request.user.is_superuser or request.user.is_staff:
        ticket_get = get_object_or_404(Tickets, id=pk)
        ticket = Tickets.objects.filter(id=pk)
        if request.method == 'POST':
            form = SupportFormAdmin(request.POST, instance=ticket_get)
            if form.is_valid():
                ticket_get.send_ticket()
                form.save()
                messages.success(request, 'Вы успешно изменили тикет!')
                return HttpResponseRedirect(reverse('mainapp:ticket_admin'))
        else:
            form = SupportFormAdmin(instance=ticket_get)
        context = {
            'title': f'Ответить на обращение',
            'ticket': ticket,
            'form': form,
        }
        return render(request, 'adminapp/tickets/send_ticket.html', context)
    else:
        return HttpResponseRedirect(reverse('mainapp:index'))


@login_required
def close_ticket_admin(request, pk):
    if request.user.is_superuser or request.user.is_staff:
        ticket_get = get_object_or_404(Tickets, id=pk)
        ticket_get.close_ticket()
        messages.success(request, 'Вы успешно закрыли тикет!')
        return HttpResponseRedirect(reverse('mainapp:ticket_admin'))
    else:
        return HttpResponseRedirect(reverse('mainapp:index'))


@login_required
def all_users(request):
    if request.user.is_superuser:
        user = User.objects.all()
        context = {
            'title': 'все пользователи',
            'user': user,
        }
        return render(request, 'adminapp/users/index.html', context)
    else:
        return HttpResponseRedirect(reverse('mainapp:index'))


@login_required
def edit_profile_admin(request, pk):
    if request.user.is_superuser:
        user = get_object_or_404(User, id=pk)
        if request.method == 'POST':
            form = ChangeFormAdmin(request.POST, instance=user)
            if form.is_valid():
                form.save()
                messages.success(request, 'Вы успешно изменили профиль!')
                return HttpResponseRedirect(reverse('mainapp:all_users'))
        else:
            form = ChangeFormAdmin(instance=user)
        context = {
            'title': 'изменить профиль',
            'form': form,
        }
        return render(request, 'mainapp/profile/edit_profile.html', context)
    else:
        return HttpResponseRedirect(reverse('mainapp:index'))


@login_required
def create_user(request):
    if request.user.is_superuser:
        if request.method == 'POST':
            form = RegisterFormAdmin(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Вы успешно создали пользователя!')
                return HttpResponseRedirect(reverse('mainapp:all_users'))
        else:
            form = RegisterFormAdmin()
        context = {
            'title': 'Создать нового пользователя',
            'form': form,
        }
        return render(request, 'adminapp/users/create_user.html', context)
    else:
        return HttpResponseRedirect(reverse('mainapp:index'))
