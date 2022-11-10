from django.forms.models import model_to_dict
from django.http import JsonResponse
from django.views.generic.detail import BaseDetailView
from django.views.generic.list import BaseListView
from movies.models import Filmwork


class MoviesApiMixin:
    model = Filmwork
    http_method_names = ['get']
    attributes = ('title',
                  'description',
                  'creation_date',
                  'rating',
                  'type')

    def get_queryset(self):
        return self.model.objects.prefetch_related('genres', 'persons')

    def render_to_response(self, context, **response_kwargs):
        return JsonResponse(context)

    def serialize(self, obj: Filmwork) -> dict:
        data = model_to_dict(obj, fields=self.attributes)

        data.update({
            'id': obj.id,
            'genres': [genre.name for genre in obj.genres.all()],
            'actors': [person.full_name for person in obj.persons.filter(
                                            personfilmwork__role='actor')],
            'directors': [person.full_name for person in obj.persons.filter(
                                            personfilmwork__role='director')],
            'writers': [person.full_name for person in obj.persons.filter(
                                            personfilmwork__role='writer')],
        })
        return data


class MoviesListApi(MoviesApiMixin, BaseListView):
    paginate_by: int = 50

    def get_context_data(self, *, object_list=None, **kwargs):
        queryset = self.get_queryset()
        paginator, page, queryset, is_paginated = self.paginate_queryset(
            queryset,
            self.paginate_by
        )
        context = {
         'count':  paginator.count,
         'total_pages': paginator.num_pages,
         'prev': page.previous_page_number() if page.has_previous() else None,
         'next': page.next_page_number() if page.has_next() else None,
         'results': [self.serialize(obj) for obj in page.object_list],
        }
        return context


class MoviesDetailApi(MoviesApiMixin, BaseDetailView):

    def get_context_data(self, object, **kwargs):
        return self.serialize(object)
