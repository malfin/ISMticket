from django.contrib.auth.models import User
from django.db import models


class UserProfile(models.Model):
    STATUS = [
        ('0', 'Пользователь'),
        ('1', 'Тех.поддержка'),
        ('2', 'Администратор'),
        ('3', 'Заблокирован'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(verbose_name='статус', choices=STATUS, default=0, max_length=128)

    def __str__(self):
        return f'{self.user}'

    def create_support(self):
        self.status = '1'
        self.save()

    def create_admin(self):
        self.status = '2'
        self.save()

    def block_user(self):
        self.status = '3'
        self.save()

    def no_block_user(self):
        self.status = '0'
        self.save()

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'


class News(models.Model):
    title = models.CharField(verbose_name='заголовок', max_length=256)
    text = models.TextField(verbose_name='текст')
    date = models.DateField(auto_now=True)

    def __str__(self):
        return self.text

    class Meta:
        ordering = ['-date'][:3]
        verbose_name = 'новость'
        verbose_name_plural = 'новости'


class Tickets(models.Model):
    STATUS = [
        ('0', 'Открыт'),
        ('1', 'Ожидает ответа'),
        ('2', 'Закрыт'),
    ]
    STATUS_CATEGORY = [
        ('0', 'Общие вопросы'),
        ('1', 'Финансовый'),
        ('2', 'Технический'),
        ('3', 'Баги/проблемы сайта'),
    ]
    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE)
    category = models.CharField(verbose_name='Выберите отдел', choices=STATUS_CATEGORY,
                                default=0, max_length=128)
    title = models.CharField(verbose_name='Тема', max_length=128)
    message = models.TextField(verbose_name='Сообщение')
    answer = models.TextField(verbose_name='Ответ от тех.поддержки', blank=True)
    status = models.CharField(verbose_name='Статус', choices=STATUS, default=0, max_length=128)
    desk = models.TextField(verbose_name='Примечание (если его нет, оставьте поле пустым)', blank=True)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.id} | {self.title}'

    def close_ticket(self):
        self.status = '2'
        self.save()

    def answer_ticket(self):
        self.status = '1'
        self.save()

    def send_ticket(self):
        self.status = '0'
        self.save()

    class Meta:
        ordering = ['-date', 'status']
        verbose_name = 'тикет'
        verbose_name_plural = 'тикеты'
