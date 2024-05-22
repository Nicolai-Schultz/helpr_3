from django.db import models
import datetime, uuid
from django.contrib.auth.models import User
from django.urls import reverse
from datetime import date
from ckeditor.fields import RichTextField


class customer(models.Model):
    first_name = models.CharField(max_length = 50)
    last_name = models.CharField(max_length = 50)
    phone = models.CharField(max_length = 10, default="",blank=True)
    email = models.EmailField(max_length = 100)
    password = models.CharField(max_length = 100)
    image = models.ImageField(upload_to='uploads/product/',blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class helpr_id(models.Model):
    customer = models.ForeignKey(customer, on_delete=models.CASCADE, default=1)
    date_creation = models.DateField(default=datetime.datetime.today)
    date_from = models.DateField()
    date_to = models.DateField()
    #   Max_digits tager også decimaler i betragtning, så 6 digits = 9999,99
    price = models.DecimalField(default=0, decimal_places=2, max_digits=6)
    #   The calculation should appear in the DB as a charfield
    #   Multiple calculations can have a relationship, maybe a boolean indicating if in relation. 
    #   Make checkbox indicating if in relation, if yes, demand helpr_id !!
    calculation = models.CharField(default="", blank=True, max_length=200)
    
    def __str__(self):
        #   You can return whatever you want here. Maybe the calculation?
        return f"{self.customer} - {self.date_creation}"
    
class Test(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    test1 = models.CharField(max_length = 50)
    test_date_fra = models.DateField(default=datetime.datetime.today)
    test_date_til = models.DateField(default=datetime.datetime.today)
    udregning_db = models.CharField(max_length = 50)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)  # ForeignKey to User model


    def __str__(self):
        return f"{self.test1}, {self.test_date_fra}, {self.test_date_til}, {self.id}"

class Hangman_category(models.Model):
    word = models.CharField(max_length = 50)

    def __str__(self):
        return self.word


class Hangman(models.Model):
    guess = models.CharField(max_length = 1, unique=True)
    
    def __str__(self):
        return f"{self.guess, self.id}"

class Team(models.Model):
    medlemmer = models.ManyToManyField(User, related_name='teams')  # Many-to-Many relationship with User model
    leder = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='team_leaders')  # ForeignKey to User model
    team_nummer = models.CharField(max_length = 2)

    def __str__(self):
        return f"Team {self.team_nummer}"

class Stats(models.Model):
    #   Issue: lige nu udfyldes user ikke auto. Dette betyder man kan override team nummer for medlem. Fiks dette.
    team = models.ForeignKey(Team, on_delete=models.CASCADE, null=True)  # ForeignKey to Team model
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)  # ForeignKey to User model

    #   Info til stats
    kpt = models.CharField(max_length = 5)
    ga = models.CharField(max_length = 5)
    kontakttilladelser = models.CharField(max_length = 5)
    csat = models.CharField(max_length = 5)
    copc = models.CharField(max_length = 5)

    kpt_2 = models.CharField(max_length = 5)
    ga_2 = models.CharField(max_length = 5)
    kontakttilladelser_2 = models.CharField(max_length = 5)
    csat_2 = models.CharField(max_length = 5)
    copc_2 = models.CharField(max_length = 5)

    kpt_3 = models.CharField(max_length = 5)
    ga_3 = models.CharField(max_length = 5)
    kontakttilladelser_3 = models.CharField(max_length = 5)
    csat_3 = models.CharField(max_length = 5)
    copc_3 = models.CharField(max_length = 5)

    #   Point til trin 
    trin_1 = models.CharField(max_length = 20)
    trin_2 = models.CharField(max_length = 20)
    trin_3 = models.CharField(max_length = 20)

    def __str__(self):
        return f"{self.user} {self.team}"

class Link(models.Model):
    name = models.CharField(max_length = 20)
    link = models.CharField(max_length = 70)

    def __str__(self):
        return f"{self.name}"

class Favorit_link(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)  # ForeignKey to User model
    all_links = models.ForeignKey(Link, on_delete=models.CASCADE, null=True)  # ForeignKey to Link model


    def __str__(self):
        return f"Favorite links"

class Post(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    body = RichTextField(blank=True, null=True)
    post_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title + "  " + str(self.author)
    
    def get_absolute_url(self):
        return reverse("article-detail", args=[str(self.id)])




#   With every change in DB do the following:
    #   Check for errors:
    #       python manage.py makemigrations
    #   Push changes to DB
            #   python manage.py migrate
    #   To display on admin site do this in admin.py:
        #   admin.site.register(NAME_OF_MODEL)