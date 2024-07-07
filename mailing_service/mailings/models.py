from django.db import models


class Client(models.Model):
    email = models.EmailField(unique=True, verbose_name='контактный email')
    name = models.CharField(max_length=100, verbose_name='Ф. И. О.')
    comment = models.TextField(blank=True, verbose_name='комментарий')

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'Клиент сервиса'
        verbose_name_plural = 'Клиенты сервиса'


class Mailing(models.Model):
    STATUS_CHOICES = [
        ('created', 'Создана'),
        ('started', 'Запущена'),
        ('completed', 'Завершена'),
    ]
    PERIOD_CHOICES = [
        ('daily', 'Ежедневно'),
        ('weekly', 'Еженедельно'),
        ('monthly', 'Ежемесячно'),
    ]
    start_date = models.DateTimeField(verbose_name='запуск рассылки')
    period = models.CharField(max_length=10, choices=PERIOD_CHOICES, verbose_name='периодичность')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='created', verbose_name='статус')
    message = models.ForeignKey('Message', on_delete=models.CASCADE)
    clients = models.ManyToManyField(Client)

    def __str__(self):
        return f'Рассылка {self.pk} - {self.status} от {self.start_date}'

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'


class Message(models.Model):
    subject = models.CharField(max_length=100, verbose_name='тема письма')
    body = models.TextField(verbose_name='сообщение')

    def __str__(self):
        return self.subject

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'


class MailingAttempt(models.Model):
    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE)
    last_attempt = models.DateTimeField(auto_now_add=True, verbose_name='последняя попытка')
    status = models.BooleanField(default=False, verbose_name='статус')
    server_response = models.TextField(blank=True, verbose_name='ответ сервера')

    def __str__(self):
        return f'Попытка {self.pk} - {"успешна" if self.status else "провалена"}'

    class Meta:
        verbose_name = 'Попытка рассылки'
        verbose_name_plural = 'Попытки рассылки'
