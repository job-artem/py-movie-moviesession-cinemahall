from datetime import datetime

from django.db.models import QuerySet

from db.models import MovieSession, Movie, CinemaHall


def create_movie_session(
        movie_show_time: datetime,
        movie_id: int,
        cinema_hall_id: int
) -> None:
    try:
        movie = Movie.objects.get(id=movie_id)
    except Movie.DoesNotExist:
        raise ValueError(f"Movie with id {movie_id} does not exist")

    try:
        cinema_hall = CinemaHall.objects.get(id=cinema_hall_id)
    except CinemaHall.DoesNotExist:
        raise ValueError(f"CinemaHall with id {cinema_hall_id} "
                         f"does not exists")

    MovieSession.objects.create(
        show_time=movie_show_time,
        movie=movie,
        cinema_hall=cinema_hall
    )


def get_movies_sessions(
        session_date: str = None
) -> QuerySet[MovieSession]:
    if session_date is not None:
        datetime_object = datetime.strptime(session_date, "%Y-%m-%d")
        return MovieSession.objects.filter(
            show_time__date=datetime_object.date()
        )
    return MovieSession.objects.all()


def get_movie_session_by_id(
        movie_session_id: int
) -> MovieSession:
    return MovieSession.objects.get(id=movie_session_id)


def update_movie_session(
        session_id: int,
        show_time: datetime = None,
        movie_id: int = None,
        cinema_hall_id: int = None
) -> None:
    session = MovieSession.objects.get(id=session_id)
    if show_time is not None:
        session.show_time = show_time
    if movie_id is not None:
        try:
            movie = Movie.objects.get(id=movie_id)
        except Movie.DoesNotExist:
            raise ValueError(f"Movie with id {movie_id} does not exist")
        session.movie = movie
    if cinema_hall_id is not None:
        session.cinema_hall_id = cinema_hall_id
    session.save()


def delete_movie_session_by_id(
        session_id: int
) -> None:
    MovieSession.objects.get(pk=session_id).delete()
