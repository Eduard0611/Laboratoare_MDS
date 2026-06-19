from django.db import models
from django.urls import reverse


class Category(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name


class Course(models.Model):
    title = models.CharField(max_length=200)
    instructor = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    year = models.IntegerField()
    semester = models.CharField(
        max_length=10,
        choices=[('fall', 'Fall'), ('spring', 'Spring')],
        default='fall',
    )
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name='courses'
    )
    credits = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.title} ({self.year})"

    def get_absolute_url(self):
        return reverse('course_detail', args=[str(self.id)])