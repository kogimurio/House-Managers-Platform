from django.db import models
from accounts.models import CustomUser
from django.db.models import Avg
from django.core.validators import MinValueValidator, MaxValueValidator

User = CustomUser

class Profile(models.Model):
    CONTRACT = (
        ('Day', 'Day'),
        ('Weeks', 'Weeks'),
        ('Months', 'Months')
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, null=True, blank=True)
    location = models.CharField(max_length=100, null=True, blank=True)
    rating = models.FloatField(default=0.0)
    image = models.ImageField(upload_to='profile_images/', null=True, blank=True)
    hobbies = models.CharField(max_length=200, null=True, blank=True)
    tribe = models.CharField(max_length=20, null=True, blank=True)
    user_type = models.CharField(max_length=20, null=True, choices=[('Employer', 'Employer'), ('HouseManager', 'HouseManager')])

    class Meta:
        abstract = True
    
    def calculate_rating(self):
        reviews = Review.objects.filter(reviewed=self.user)
        self.rating = reviews.aggregate(Avg('rating'))['rating__avg'] or 0.0
        self.save()


class Employer(Profile):
    house_type = models.CharField(max_length=100, null=True, blank=True)
    number_rooms = models.IntegerField(null=True)
    number_people = models.IntegerField(null=True)
    number_children = models.IntegerField(null=True, blank=True)
    preferred_contract_duration = models.CharField(max_length=20, choices=Profile.CONTRACT, null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} (Employer)"

class HouseManager(Profile):
    AVAILABILITY = (
        ('Immediately', 'Immediately'),
        ('Next-Week', 'Next-Week'),
        ('Next-Month', 'Next-Month')
    )
    GENDER = (
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other')
    )
    education = models.CharField(max_length=100, null=True, blank=True)
    availability = models.CharField(max_length=100, null=True, choices=AVAILABILITY)
    years_of_experience = models.PositiveIntegerField(null=True, blank=True, default=0)
    skills = models.TextField(null=True, blank=True)
    age = models.PositiveIntegerField(null=True,)
    certifications = models.TextField(null=True, blank=True)
    languages_spoken = models.CharField(max_length=100, null=True, blank=True)
    expected_salary = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    marital_status = models.CharField(max_length=100, null=True, blank=True)
    income = models.CharField(max_length=100, null=True, blank=True)
    occupation = models.CharField(max_length=100, null=True, blank=True)
    gender = models.CharField(max_length=10, choices=GENDER, null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} (House Manager)"

class Review(models.Model):
    reviewer = models.ForeignKey(User, related_name='reviews_giver', on_delete=models.CASCADE)
    reviewed = models.ForeignKey(User, related_name='reviews_receiver', on_delete=models.CASCADE)
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField(max_length=500, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('reviewer','reviewed')
    
    def __str__(self):
        return f"{self.reviewer.username} for {self.reviewed.username}"
    

