from src.api.models.base import FilmFullMixin, FilmMixin


class Film(FilmFullMixin):
    pass


class FilmForFilmsList(FilmMixin):
    pass
