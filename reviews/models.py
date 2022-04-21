from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse

from accounts.models import Account


class ReviewSchool(models.Model):
    review_account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='review_school')
    review = models.TextField()
    purity = models.IntegerField(
        validators=[MinValueValidator(1),
                    MaxValueValidator(10)],
        default=0,
        verbose_name='чистота'
    )
    nutrition = models.IntegerField(
        validators=[MinValueValidator(1),
                    MaxValueValidator(10)],
        default=0,
        verbose_name='питание'
    )
    training_program = models.IntegerField(
        validators=[MinValueValidator(1),
                    MaxValueValidator(10)],
        default=0,
        verbose_name='программа обучения'
    )
    security = models.IntegerField(
        validators=[MinValueValidator(1),
                    MaxValueValidator(10)],
        default=0,
        verbose_name='безопасность')
    locations = models.IntegerField(
        validators=[MinValueValidator(1),
                    MaxValueValidator(10)],
        default=0,
        verbose_name='локации')
    office = models.IntegerField(
        validators=[MinValueValidator(1),
                    MaxValueValidator(10)],
        default=0,
        verbose_name='здание')
    quality_of_education = models.IntegerField(
        validators=[MinValueValidator(1),
                    MaxValueValidator(10)],
        default=0,
        verbose_name='качество образования')
    price_and_quality = models.IntegerField(
        validators=[MinValueValidator(1),
                    MaxValueValidator(10)],
        default=0,
        verbose_name='цена и качество')

    study_guides = models.IntegerField(
        validators=[MinValueValidator(1),
                    MaxValueValidator(10)],
        default=0,
        verbose_name='учебные пособия')
    update = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def rating_average(self):
        avg = (
            self.purity
            + self.nutrition
            + self.training_program
            + self.security
            + self.locations
            + self.office
            + self.quality_of_education
            + self.price_and_quality
            + self.study_guides
        ) / 9
        return round(avg, 1)

    rating_average.short_description = "Avg."

    def __str__(self):
        return f"{self.review}"

    def get_absolute_url(self):
        return reverse('detail_school', kwargs={'pk': self.pk})


class ReviewOffice(models.Model):
    review_account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='review_office')
    review = models.TextField()
    reputation = models.IntegerField(
        validators=[MinValueValidator(1),
                    MaxValueValidator(10)],
        default=0,
        verbose_name='репутация')
    staff = models.IntegerField(
        validators=[MinValueValidator(1),
                    MaxValueValidator(10)],
        default=0,
        verbose_name='персонал')
    support = models.IntegerField(
        validators=[MinValueValidator(1),
                    MaxValueValidator(10)],
        default=0,
        verbose_name='поддержка')
    accompany = models.IntegerField(
        validators=[MinValueValidator(1),
                    MaxValueValidator(10)],
        default=0,
        verbose_name='сопровождение')
    efficiency = models.IntegerField(
        validators=[MinValueValidator(1),
                    MaxValueValidator(10)],
        default=0,
        verbose_name='эффективность')
    price_and_quality = models.IntegerField(
        validators=[MinValueValidator(1),
                    MaxValueValidator(10)],
        default=0,
        verbose_name='цена и качество')
    update = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def rating_average(self):
        avg = (
            self.reputation
            + self.staff
            + self.support
            + self.accompany
            + self.efficiency
            + self.price_and_quality
        ) / 6
        return round(avg, 1)

    rating_average.short_description = "Avg."

    def __str__(self):
        return f"{self.review}"

    def get_absolute_url(self):
        return reverse('detail_office', kwargs={'pk': self.pk})


class ReviewKindergarten(models.Model):
    review_account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='review_cat_kindergarten')
    review = models.TextField()
    purity = models.IntegerField(
        validators=[MinValueValidator(1),
                    MaxValueValidator(10)],
        default=0,
        verbose_name='чистота'
    )
    nutrition = models.IntegerField(
        validators=[MinValueValidator(1),
                    MaxValueValidator(10)],
        default=0,
        verbose_name='питание'
    )
    activity = models.IntegerField(
        validators=[MinValueValidator(1),
                    MaxValueValidator(10)],
        default=0,
        verbose_name='активность')
    upbringing = models.IntegerField(
        validators=[MinValueValidator(1),
                    MaxValueValidator(10)],
        default=0,
        verbose_name='воспитание')
    security = models.IntegerField(
        validators=[MinValueValidator(1),
                    MaxValueValidator(10)],
        default=0,
        verbose_name='безопасность')
    locations = models.IntegerField(
        validators=[MinValueValidator(1),
                    MaxValueValidator(10)],
        default=0,
        verbose_name='локации')
    office = models.IntegerField(
        validators=[MinValueValidator(1),
                    MaxValueValidator(10)],
        default=0,
        verbose_name='здание')
    baby_care = models.IntegerField(
        validators=[MinValueValidator(1),
                    MaxValueValidator(10)],
        default=0,
        verbose_name='уход за ребенком')
    price_and_quality = models.IntegerField(
        validators=[MinValueValidator(1),
                    MaxValueValidator(10)],
        default=0,
        verbose_name='цена и качество')
    update = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def rating_average(self):
        avg = (
            self.purity
            + self.nutrition
            + self.activity
            + self.upbringing
            + self.security
            + self.locations
            + self.office
            + self.baby_care
            + self.price_and_quality
        ) / 9
        return round(avg, 1)

    rating_average.short_description = "Avg."

    def __str__(self):
        return f"{self.review}"

    def get_absolute_url(self):
        return reverse('detail_kindergarten', kwargs={'pk': self.pk})
