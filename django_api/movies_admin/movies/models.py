import uuid
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _


class TimeStampedMixin(models.Model):
    created = models.DateTimeField(_('Created'), auto_now_add=True)
    modified = models.DateTimeField(_('Modified'), auto_now=True)

    class Meta:
        abstract = True


class UUIDMixin(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class Genre(UUIDMixin, TimeStampedMixin):
    name = models.CharField(_('Name'), max_length=100)
    description = models.TextField(_('Description'), blank=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "content\".\"genre"
        verbose_name = _('genre')
        verbose_name_plural = _('Genres')


class Person(UUIDMixin, TimeStampedMixin):
    full_name = models.CharField(_('Full name'), max_length=255)

    def __str__(self):
        return self.full_name

    class Meta:
        db_table = "content\".\"person"
        verbose_name = _('Person')
        verbose_name_plural = _('Persons')


class Filmwork(UUIDMixin, TimeStampedMixin):

    class TypesFilmwork(models.TextChoices):
        MOVIE = 'movie', _('Movie')
        TVSHOW = 'tv_show', _('Tv Show')

    title = models.TextField(_('Title'))
    description = models.TextField(_('Description'), blank=True)
    creation_date = models.DateTimeField(_('Creation date'))
    rating = models.FloatField(_('Rating'), blank=True,
                               validators=[MinValueValidator(0),
                                           MaxValueValidator(100)])
    type = models.TextField(_('Type'),
                            choices=TypesFilmwork.choices,)
    certificate = models.CharField(_('certificate'), max_length=512,
                                   blank=True)
    file_path = models.FileField(_('file'), blank=True, null=True,
                                 upload_to='movies/')
    genres = models.ManyToManyField(Genre, through='GenreFilmwork')
    persons = models.ManyToManyField(Person, through='PersonFilmwork')

    def __str__(self):
        return self.title

    class Meta:
        db_table = "content\".\"film_work"
        verbose_name = _('Filmwork')
        verbose_name_plural = _('Filmworks')


class GenreFilmwork(UUIDMixin):
    film_work = models.ForeignKey('Filmwork', on_delete=models.CASCADE)
    genre = models.ForeignKey('Genre', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "content\".\"genre_film_work"
        indexes = [
            models.Index(fields=['film_work_id', 'genre_id'],
                         name='film_work_genre_idx'),
        ]
        unique_together = ['film_work_id', 'genre_id']


class PersonFilmwork(UUIDMixin):
    class RoleTypes(models.TextChoices):
        ACTOR = 'actor', _('Actor')
        WRITER = 'writer', _('Writer')
        DIRECTOR = 'director', _('Director')

    film_work = models.ForeignKey('Filmwork', on_delete=models.CASCADE)
    person = models.ForeignKey('Person', on_delete=models.CASCADE)
    role = models.TextField(_('Role'), null=True,
                            choices=RoleTypes.choices,)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "content\".\"person_film_work"
        indexes = [
            models.Index(fields=['film_work_id', 'person_id', 'role'],
                         name='film_work_person_idx'),
        ]
        unique_together = ['film_work_id', 'person_id', 'role']
