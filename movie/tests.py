import json
from django.test import TestCase, Client
from .models import Movie, MovieGenre, MovieActor, Rating, Country, Genre, Actor


class MovieTest(TestCase):
    maxDiff = None

    def setUp(self):
        Country.objects.create(
            id=1,
            name='한국'
        )
        Rating.objects.create(
            id=1,
            name='15세 관람가'
        )
        Rating.objects.create(
            id=2,
            name='12세 관람가'
        )
        Movie.objects.create(
            id=1,
            name='조제',
            country_id=1,
            running_time=117,
            release_date='2020-12-10',
            director='김종관',
            rating_id=1,
            image='test.jpg',
            summary='자신을 ‘조제’로 불러달라는 그녀/n처음 만난 그날부터 ‘조제’는 ‘영석’에게 잊을 수 없는 이름으로 남는다.'
        )
        Movie.objects.create(
            id=2,
            name='이웃사촌',
            country_id=1,
            running_time=130,
            release_date='2020-11-25',
            director='이환경',
            rating_id=2,
            image='test1.jpg',
            summary='적인가, 이웃인가?/n 낮에는 친근한 이웃집 vs 밤에는 수상한 도청팀'
        )
        Genre.objects.create(
            id=1,
            name='멜로/로맨스'
        )
        Genre.objects.create(
            id=2,
            name='드라마'
        )
        Genre.objects.create(
            id=3,
            name='코미디'
        )
        MovieGenre.objects.create(
            id=1,
            movie_id=1,
            genre_id=1
        )
        MovieGenre.objects.create(
            id=2,
            movie_id=1,
            genre_id=2
        )
        MovieGenre.objects.create(
            id=3,
            movie_id=2,
            genre_id=2
        )
        MovieGenre.objects.create(
            id=4,
            movie_id=2,
            genre_id=3
        )
        Actor.objects.create(
            id=1,
            name='한지민'
        )
        Actor.objects.create(
            id=2,
            name='남주혁'
        )
        Actor.objects.create(
            id=3,
            name='정우'
        )
        Actor.objects.create(
            id=4,
            name='오달수'
        )
        Actor.objects.create(
            id=5,
            name='김희원'
        )
        MovieActor.objects.create(
            id=1,
            movie_id=1,
            actor_id=1
        )
        MovieActor.objects.create(
            id=2,
            movie_id=1,
            actor_id=2
        )
        MovieActor.objects.create(
            id=3,
            movie_id=2,
            actor_id=3
        )
        MovieActor.objects.create(
            id=4,
            movie_id=2,
            actor_id=4
        )
        MovieActor.objects.create(
            id=5,
            movie_id=2,
            actor_id=5
        )

    def tearDown(self):
        Movie.objects.all().delete()
        MovieGenre.objects.all().delete()
        MovieActor.objects.all().delete()
        Actor.objects.all().delete()
        Genre.objects.all().delete()
        Country.objects.all().delete()
        Rating.objects.all().delete()

    def test_get_movie_list_success(self):
        client = Client()

        response = client.get('/movies')
        self.assertEqual(response.json(),
                         {
                             'message': 'Success',
                             'movie_list': [
                                 {
                                     'movie_id': 1,
                                     'name': '조제',
                                     'country': '한국',
                                     'running_time': 117,
                                     'release_date': '2020-12-10',
                                     'director': '김종관',
                                     'rating': '15세 관람가',
                                     'image': 'test.jpg',
                                     'summary': '자신을 ‘조제’로 불러달라는 그녀/n처음 만난 그날부터 ‘조제’는 ‘영석’에게 잊을 수 없는 '
                                                '이름으로 남는다.',
                                     'audience_score': '0.00',
                                     'netizen_score': '0.00',
                                     'reporter_critic_score': '0.00',
                                     'actor': ['한지민', '남주혁'],
                                     'genre': ['멜로/로맨스', '드라마']
                                 },
                                 {
                                     'movie_id': 2,
                                     'name': '이웃사촌',
                                     'country': '한국',
                                     'running_time': 130,
                                     'release_date': '2020-11-25',
                                     'director': '이환경',
                                     'rating': '12세 관람가',
                                     'image': 'test1.jpg',
                                     'summary': '적인가, 이웃인가?/n 낮에는 친근한 이웃집 vs 밤에는 수상한 도청팀',
                                     'audience_score': '0.00',
                                     'netizen_score': '0.00',
                                     'reporter_critic_score': '0.00',
                                     'actor': ['정우', '오달수', '김희원'],
                                     'genre': ['드라마', '코미디']
                                 }
                             ]
                         })
        self.assertEqual(response.status_code, 200)

    def test_post_movie_data_success(self):
        client = Client()

        movie_data = {
            'name': '런',
            'country': '미국',
            'running_time': 90,
            'release_date': '20201120',
            'director': '아니쉬 차간티',
            'rating': '15세 관람가',
            'image': 'test2.jpg',
            'summary': '가장 안전했던 그곳이 가장 위험한 공간이 된다!',
            'genre': ['미스터리', '스릴러'],
            'actor': ['사라 폴슨', '키에라 앨런']
        }

        response = client.post('/movies', json.dumps(movie_data), content_type='application/json')
        self.assertEqual(response.json(), {'message': 'Created'})
        self.assertEqual(response.status_code, 201)

    def test_post_movie_data_conflict(self):
        client = Client()

        movie_data = {
            'name': '조제',
            'country': '미국',
            'running_time': 90,
            'release_date': '20201120',
            'director': '김종관',
            'rating': '15세 관람가',
            'image': 'test2.jpg',
            'summary': '가장 안전했던 그곳이 가장 위험한 공간이 된다!',
            'genre': ['미스터리', '스릴러'],
            'actor': ['사라 폴슨', '키에라 앨런']
        }

        response = client.post('/movies', json.dumps(movie_data), content_type='application/json')
        self.assertEqual(response.json(), {'message': 'Conflict'})
        self.assertEqual(response.status_code, 409)

    def test_post_movie_data_key_error(self):
        client = Client()

        movie_data = {
            'name': '미드나이트 스카이',
            'countr': '미국',
            'running_time': 118,
            'release_date': '20201209',
            'director': '조지 클루니',
            'rating': '12세 관람가',
            'image': 'test2.jpg',
            'summary': '가장 안전했던 그곳이 가장 위험한 공간이 된다!',
            'genre': ['미스터리', '스릴러'],
            'actor': ['사라 폴슨', '키에라 앨런']
        }

        response = client.post('/movies', json.dumps(movie_data), content_type='application/json')
        self.assertEqual(response.json(), {'message': 'Key Error'})
        self.assertEqual(response.status_code, 400)

    def test_put_movie_data_success(self):
        client = Client()

        movie_data = [{
                'movie_id': 1,
                'name': '조제',
                'country': '한국',
                'running_time': 120,
                'release_date': '20201210',
                'director': '김종관',
                'rating': '15세 관람가',
                'image': 'test2.jpg',
                'summary': '가장 안전했던 그곳이 가장 위험한 공간이 된다!',
                'genre': ['미스터리', '스릴러'],
                'actor': ['사라 폴슨', '키에라 앨런']
            },
            {
                'movie_id': 2,
                'name': '이웃사촌',
                'country': '한국',
                'running_time': 120,
                'release_date': '20201210',
                'director': '김종관',
                'rating': '15세 관람가',
                'image': 'test2.jpg',
                'summary': '가장 안전했던 그곳이 가장 위험한 공간이 된다!',
                'genre': ['미스터리', '스릴러'],
                'actor': ['사라 폴슨', '키에라 앨런']
            }]

        response = client.put('/movies', json.dumps(movie_data), content_type='application/json')
        self.assertEqual(response.json(), {'message': 'Accepted'})
        self.assertEqual(response.status_code, 202)

    def test_put_movie_data_key_error(self):
        client = Client()

        movie_data = [{
            'movie_id': 1,
            'name': '조제',
            'county': '한국',
            'running_time': 120,
            'release_date': '20201210',
            'director': '김종관',
            'rating': '15세 관람가',
            'image': 'test2.jpg',
            'summary': '가장 안전했던 그곳이 가장 위험한 공간이 된다!',
            'genre': ['미스터리', '스릴러'],
            'actor': ['사라 폴슨', '키에라 앨런']
        },
            {
                'movie_id': 2,
                'name': '이웃사촌',
                'country': '한국',
                'running_time': 120,
                'release_date': '20201210',
                'director': '김종관',
                'rating': '15세 관람가',
                'image': 'test2.jpg',
                'summary': '가장 안전했던 그곳이 가장 위험한 공간이 된다!',
                'genre': ['미스터리', '스릴러'],
                'actor': ['사라 폴슨', '키에라 앨런']
        }]

        response = client.put('/movies', json.dumps(movie_data), content_type='application/json')
        self.assertEqual(response.json(), {'message': 'Key Error'})
        self.assertEqual(response.status_code, 400)

    def test_put_movie_data_not_found(self):
        client = Client()

        movie_data = [{
            'movie_id': 7,
            'name': '조제',
            'country': '한국',
            'running_time': 120,
            'release_date': '20201210',
            'director': '김종관',
            'rating': '15세 관람가',
            'image': 'test2.jpg',
            'summary': '가장 안전했던 그곳이 가장 위험한 공간이 된다!',
            'genre': ['미스터리', '스릴러'],
            'actor': ['사라 폴슨', '키에라 앨런']
        },
            {
                'movie_id': 2,
                'name': '이웃사촌',
                'country': '한국',
                'running_time': 120,
                'release_date': '20201210',
                'director': '김종관',
                'rating': '15세 관람가',
                'image': 'test2.jpg',
                'summary': '가장 안전했던 그곳이 가장 위험한 공간이 된다!',
                'genre': ['미스터리', '스릴러'],
                'actor': ['사라 폴슨', '키에라 앨런']
            }]

        response = client.put('/movies', json.dumps(movie_data), content_type='application/json')
        self.assertEqual(response.json(), {'message': 'Not found'})
        self.assertEqual(response.status_code, 404)

    def test_put_movie_data_not_acceptable(self):
        client = Client()

        movie_data = [{
            'movie_id': 1,
            'name': '조제',
            'country': '한국',
            'running_time': 120,
            'release_date': '20201210',
            'director': '김종관',
            'rating': '15세 관람가',
            'image': 'test2.jpg',
            'summary': '가장 안전했던 그곳이 가장 위험한 공간이 된다!',
            'genre': ['미스터리', '스릴러'],
            'actor': ['사라 폴슨', '키에라 앨런']
        },
            {
                'movie_id': 2,
                'name': '이웃사촌',
                'country': '한국',
                'running_time': 120,
                'release_date': '20201210',
                'director': '김종관',
                'rating': '15세 관람가',
                'image': 'test2.jpg',
                'summary': '가장 안전했던 그곳이 가장 위험한 공간이 된다!',
                'genre': ['미스터리', '스릴러'],
                'actor': ['사라 폴슨', '키에라 앨런']
            }]

        response = client.put('/movies', json.dumps(movie_data), content_type='text')
        self.assertEqual(response.json(), {'message': 'Not acceptable'})
        self.assertEqual(response.status_code, 406)

    def test_delete_movie_data_success(self):
        client = Client()

        response = client.delete('/movies')
        self.assertEqual(response.status_code, 204)


class MovieDetailTest(TestCase):
    maxDiff = None

    def setUp(self):
        Country.objects.create(
            id=1,
            name='한국'
        )
        Rating.objects.create(
            id=1,
            name='15세 관람가'
        )
        Rating.objects.create(
            id=2,
            name='12세 관람가'
        )
        Movie.objects.create(
            id=1,
            name='조제',
            country_id=1,
            running_time=117,
            release_date='2020-12-10',
            director='김종관',
            rating_id=1,
            image='test.jpg',
            summary='자신을 ‘조제’로 불러달라는 그녀/n처음 만난 그날부터 ‘조제’는 ‘영석’에게 잊을 수 없는 이름으로 남는다.'
        )
        Movie.objects.create(
            id=2,
            name='이웃사촌',
            country_id=1,
            running_time=130,
            release_date='2020-11-25',
            director='이환경',
            rating_id=2,
            image='test1.jpg',
            summary='적인가, 이웃인가?/n 낮에는 친근한 이웃집 vs 밤에는 수상한 도청팀'
        )
        Genre.objects.create(
            id=1,
            name='멜로/로맨스'
        )
        Genre.objects.create(
            id=2,
            name='드라마'
        )
        Genre.objects.create(
            id=3,
            name='코미디'
        )
        MovieGenre.objects.create(
            id=1,
            movie_id=1,
            genre_id=1
        )
        MovieGenre.objects.create(
            id=2,
            movie_id=1,
            genre_id=2
        )
        MovieGenre.objects.create(
            id=3,
            movie_id=2,
            genre_id=2
        )
        MovieGenre.objects.create(
            id=4,
            movie_id=2,
            genre_id=3
        )
        Actor.objects.create(
            id=1,
            name='한지민'
        )
        Actor.objects.create(
            id=2,
            name='남주혁'
        )
        Actor.objects.create(
            id=3,
            name='정우'
        )
        Actor.objects.create(
            id=4,
            name='오달수'
        )
        Actor.objects.create(
            id=5,
            name='김희원'
        )
        MovieActor.objects.create(
            id=1,
            movie_id=1,
            actor_id=1
        )
        MovieActor.objects.create(
            id=2,
            movie_id=1,
            actor_id=2
        )
        MovieActor.objects.create(
            id=3,
            movie_id=2,
            actor_id=3
        )
        MovieActor.objects.create(
            id=4,
            movie_id=2,
            actor_id=4
        )
        MovieActor.objects.create(
            id=5,
            movie_id=2,
            actor_id=5
        )

    def tearDown(self):
        Movie.objects.all().delete()
        MovieGenre.objects.all().delete()
        MovieActor.objects.all().delete()
        Actor.objects.all().delete()
        Genre.objects.all().delete()
        Country.objects.all().delete()
        Rating.objects.all().delete()

    def test_get_movie_data_success(self):
        client = Client()

        response = client.get('/movies/1')

        self.assertEqual(response.json(),
                         {
                             'message': 'Success',
                             'movie_data':
                                 {
                                     'movie_id': 1,
                                     'name': '조제',
                                     'country': '한국',
                                     'running_time': 117,
                                     'release_date': '2020-12-10',
                                     'director': '김종관',
                                     'rating': '15세 관람가',
                                     'image': 'test.jpg',
                                     'summary': '자신을 ‘조제’로 불러달라는 그녀/n처음 만난 그날부터 ‘조제’는 ‘영석’에게 잊을 수 없는 '
                                                '이름으로 남는다.',
                                     'audience_score': '0.00',
                                     'netizen_score': '0.00',
                                     'reporter_critic_score': '0.00',
                                     'actor': ['한지민', '남주혁'],
                                     'genre': ['멜로/로맨스', '드라마']
                                 }
                         })
        self.assertEqual(response.status_code, 200)

    def test_get_movie_data_not_found(self):
        client = Client()

        response = client.get('/movies/10')

        self.assertEqual(response.json(), {'message': 'Not found'})
        self.assertEqual(response.status_code, 404)
