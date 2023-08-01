from django.db import models
from courses.models import Course


class Order(models.Model):
    user = models.ForeignKey("users.Student", on_delete=models.CASCADE, null=False)
    order_date = models.DateTimeField(auto_now_add=True)
    courses = models.ManyToManyField("courses.Course", related_name='orders')

    def __str__(self) -> str:
        return str(self.user.user.username)

    def update_participants(self):
        # Отримати список курсів, пов'язаних з ордером
        courses = self.courses.all()

        for course in courses:
            if self.pk:  # Якщо ордер уже існує (оновлення)
                # Перевірити, чи ордер був змінений та видалений
                try:
                    old_order = Order.objects.get(pk=self.pk)
                except Order.DoesNotExist:
                    break  # Якщо ордер був видалений, просто перервати цикл

                if course not in old_order.courses.all():
                    # Курс був доданий до ордера, додати учасника
                    course.participants.add(self.user)
                elif course not in self.courses.all():
                    # Курс був видалений з ордера, видалити учасника
                    course.participants.remove(self.user)

            else:  # Якщо ордер ще не існує (створення)
                course.participants.add(self.user)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.update_participants()

    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)
        self.update_participants()
