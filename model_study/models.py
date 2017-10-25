# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Person(models.Model):
    id = models.AutoField(primary_key=True)
    SHIRT_SIZES = (
        ('L', 'Large'),
        ('M', 'Medium'),
        ('S', 'Small'),
    )
    first_name = models.CharField('First Name', max_length=30)
    last_name = models.CharField('Last Name', max_length=30)
    age = models.IntegerField('Age', default=0)
    shirt_size = models.CharField('Shirt Size', choices=SHIRT_SIZES, max_length=1, default='S')
    birth_date = models.DateField('Birth Date', auto_now=True)

    def baby_boomer_status(self):
        """Return the person's baby-boomber status."""
        import datetime
        if self.birth_date < datetime.date(1945,8,1):
            return "Pre-boomer"
        elif self.birth_date > datetime.date(1965, 1, 1):
            return "Baby boomer"
        else:
            print("help")
            return "Post boomer"

    def _get_full_name(self):
        """Retruns the person's full name."""
        return "%s %s"%(self.first_name, self.last_name)

    full_name = property(_get_full_name)

    def __str__(self):
        return "%s %s"%(self.first_name, self.last_name)

class Group(models.Model):
    name = models.CharField('Group',max_length=20)
    members = models.ManyToManyField(Person, through='Membership')
    def __str__(self):
        return self.name
class Membership(models.Model):
    person = models.ForeignKey(Person)
    group = models.ForeignKey(Group)
    date_joined = models.DateField()
    invite_reason = models.CharField("Invite Reason", max_length=100)
    def __str__(self):
        return "Membership"

class Fruit(models.Model):
    name = models.CharField('Name', max_length=100, primary_key=True)
    def __str__(self):
        return self.name

class Musician(models.Model):
    first_name = models.CharField('First Name', max_length=50)
    last_name = models.CharField('Last Name', max_length=50)
    instrument = models.CharField('Instrument', max_length=100)
    def __str__(self):
        return "%s %s"%(self.first_name, self.last_name)

class Album(models.Model):
    artist = models.ForeignKey(Musician)
    name = models.CharField('Album Name', max_length=50)
    release_date = models.DateField()
    num_stars = models.IntegerField('Stars Number',default=0)
    def __str__(self):
        return self.name

class Manufacturer(models.Model):
    pass

class Car(models.Model):
    manufacturer = models.ForeignKey(Manufacturer)

class Topping(models.Model):
    pass

class Pizza(models.Model):
    toppings = models.ManyToManyField(Topping)

class Ox(models.Model):
    horn_length = models.IntegerField("horn lenth")
    class Meta:
        ordering = ["horn_length"]
        verbose_name_plural = "oxen"


