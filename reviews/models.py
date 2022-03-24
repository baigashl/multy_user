from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
# from core import models as core_models


class Review(models.Model):

    """ Review Model Definition """

    review = models.TextField()
    nutrition = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )
    security = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )
    program = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )
    cleanliness = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )
    teacher = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )
    user = models.ForeignKey(
        "users.CustomUser", related_name="reviews", on_delete=models.CASCADE
    )
    account = models.ForeignKey(
        "accounts.Account", related_name="reviews", on_delete=models.CASCADE
    )
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.review} - {self.account}"

    def rating_average(self):
        avg = (
            self.nutrition
            + self.security
            + self.cleanliness
            + self.program
            + self.teacher
        ) / 5
        return round(avg, 2)

    rating_average.short_description = "Avg."

    class Meta:
        ordering = ("-created",)
