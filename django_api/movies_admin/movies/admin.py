from django.contrib import admin
from .models import Genre, Filmwork, GenreFilmwork, Person, \
    PersonFilmwork


class GenreFilmworkInline(admin.TabularInline):
    model = GenreFilmwork


class PersonFilmworkInline(admin.TabularInline):
    model = PersonFilmwork


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name',)

    search_fields = ('name', 'description', 'id')



@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ('full_name',)

    search_fields = ('full_name', 'id')


@admin.register(Filmwork)
class FilmworkAdmin(admin.ModelAdmin):
    inlines = (GenreFilmworkInline, PersonFilmworkInline)
    list_prefetch_related = ['genres', 'persons']
    list_display = ('title', 'type', 'creation_date', 'rating', )

    list_filter = ('type', 'creation_date',)

    search_fields = ('title', 'description', 'id')

    def get_queryset(self, request):
        queryset = (
                    super()
                    .get_queryset(request)
                    .prefetch_related(*self.list_prefetch_related)
        )
        return queryset
