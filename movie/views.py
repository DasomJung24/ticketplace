import json
from datetime import date, datetime
from django.views import View
from django.http import JsonResponse
from .models import Movie, Country, Rating, MovieActor, MovieGenre, Genre, Actor
from .decorator import content_type


class MovieView(View):
    def get(self, request):
        """ 영화 리스트 api

        영화 데이터 리스트 받아오기

        Returns:
            200 : Success, movie_list (type:dict)
            404 : Not found, 영화 리스트가 없을 때
            500 : exception

        """
        try:
            movies = Movie.objects.all().select_related('country').select_related('rating')
            if movies is None:
                return JsonResponse({'message': 'Not found'}, status=404)

            results = [{
                'movie_id': data.id,
                'name': data.name,
                'country': data.country.name,
                'running_time': data.running_time,
                'release_date': data.release_date.strftime('%Y-%m-%d'),
                'director': data.director,
                'rating': data.rating.name,
                'image': data.image,
                'summary': data.summary,
                'audience_score': data.audience_score,
                'netizen_score': data.netizen_score,
                'reporter_critic_score': data.reporter_critic_score,
                'actor': [data.actor.name for data in MovieActor.objects.filter(movie=data)],
                'genre': [data.genre.name for data in MovieGenre.objects.filter(movie=data)]
            } for data in movies]

            return JsonResponse({'message': 'Success', 'movie_list': results}, status=200)

        except Exception as e:
            return JsonResponse({'message': '{}'.format(e)}, status=500)

    @content_type
    def post(self, request):
        """ 영화 등록 api

        영화 정보 등록을 위한 데이터를 Body 에 받음

        Args:
            request:
                name : 영화 제목, str
                country : 국가, str
                running_time : 상영 시간, int
                release_date : 개봉 날짜, str
                director : 감독, str
                rating : 등급(15세 관람가, 12세 관람가 등), str
                image : 포스터 이미지, url
                summary : 줄거리, str
                genre : 장르, list
                actor : 배우, list

        Returns:
            201 : created 영화 등록 성공 시
            409 : conflict 같은 영화가 이미 등록되어 있을 경우
            400 : key error
            500 : exception

        """
        try:
            data = json.loads(request.body)

            if Movie.objects.filter(name=data['name'], director=data['director']).exists():
                return JsonResponse({'message': 'Conflict'}, status=409)

            country, flag = Country.objects.get_or_create(name=data['country'])
            rating, flag = Rating.objects.get_or_create(name=data['rating'])

            movie = Movie.objects.create(
                name=data['name'],
                country=country,
                running_time=data['running_time'],
                release_date=datetime.strptime(data['release_date'], '%Y%m%d').date(),
                director=data['director'],
                rating=rating,
                image=data['image'],
                summary=data['summary']
            )

            for gen in data['genre']:
                genre, flag = Genre.objects.get_or_create(name=gen)
                MovieGenre.objects.create(movie_id=movie.id, genre_id=genre.id)

            for act in data['actor']:
                actor, flag = Actor.objects.get_or_create(name=act)
                MovieActor.objects.create(movie_id=movie.id, actor_id=actor.id)

            return JsonResponse({'message': 'Created'}, status=201)

        except KeyError:
            return JsonResponse({'message': 'Key Error'}, status=400)
        except Exception as e:
            return JsonResponse({'message': '{}'.format(e)}, status=500)

    @content_type
    def put(self, request):
        """영화 상세페이지 수정 api

        body 로 정보를 수정하려는 영화의 id 와 데이터 받아와 수정하기

        Args:
            request:
                movie_id : 영화 id
                name : 영화 제목, str
                country : 국가, str
                running_time : 상영 시간, int
                release_date : 개봉 날짜, str
                director : 감독, str
                rating : 등급(15세 관람가, 12세 관람가 등), str
                image : 포스터 이미지, url
                summary : 줄거리, str
                genre : 장르, list
                actor : 배우, list

        Returns:
            202 : Accepted, 요청이 접수되었을 때
            400 : Key error
            404 : Not found, id에 해당하는 영화의 정보가 없을 때
            406 : Not acceptable, header 의 content-type 이 상이할 때
            500 : exception

        """
        try:
            data = json.loads(request.body)

            if not Movie.objects.filter(id=data['movie_id']).exists():
                return JsonResponse({'message': 'Not found'}, status=404)

            country, flag = Country.objects.get_or_create(name=data['country'])
            rating, flag = Rating.objects.get_or_create(name=data['rating'])

            MovieActor.objects.filter(movie_id=data['movie_id']).delete()
            MovieGenre.objects.filter(movie_id=data['movie_id']).delete()

            movie = Movie.objects.get(id=data['movie_id'])
            movie.name = data['name']
            movie.country = country
            movie.running_time = data['running_time']
            movie.release_date = datetime.strptime(data['release_date'], '%Y%m%d').date()
            movie.director = data['director']
            movie.rating = rating
            movie.image = data['image']
            movie.summary = data['summary']
            movie.save()

            for gen in data['genre']:
                genre, flag = Genre.objects.get_or_create(name=gen)
                MovieGenre.objects.create(movie_id=data['movie_id'], genre_id=genre.id)

            for act in data['actor']:
                actor, flag = Actor.objects.get_or_create(name=act)
                MovieActor.objects.create(movie_id=data['movie_id'], actor_id=actor.id)

            return JsonResponse({'message': 'Accepted'}, status=202)

        except KeyError:
            return JsonResponse({'message': 'Key Error'}, status=400)
        except Exception as e:
            return JsonResponse({'message': '{}'.format(e)}, status=500)

    def delete(self, request):
        """영화 정보 삭제 api

        body 에 삭제하려는 영화의 id 받아와서 데이터 삭제하기

        Args:
            request:
                movie_id : 영화 id

        Returns:
            204 : No contents, 삭제가 정상적으로 이루어졌을 때
            400 : Key Error
            404 : Not found, id 에 해당하는 영화 데이터가 없을 때
            500 : exception
        """
        try:
            movie_id = request.GET.get('movie_id', None)

            if not Movie.objects.filter(id=movie_id).exists():
                return JsonResponse({'message': 'Not found'}, status=404)

            Movie.objects.get(id=movie_id).delete()

            return JsonResponse({'message': 'No contents'}, status=204)

        except Exception as e:
            return JsonResponse({'message': '{}'.format(e)}, status=500)


class MovieDetailView(View):
    def get(self, request, movie_id):
        """영화 상세페이지 api

        path params 로 영화 id 값을 받아서 상세페이지 데이터 불러오기

        Args:
            request:
            movie_id: 영화 id

        Returns:
            200 : Success, movie_data (type:dict)
            404 : Not found, id에 해당하는 영화 정보가 없을 때
            500 : exception

        """
        try:
            if not Movie.objects.filter(id=movie_id).exists():
                return JsonResponse({'message': 'Not found'}, status=404)

            movie = Movie.objects.get(id=movie_id)
            result = {
                'movie_id': movie_id,
                'name': movie.name,
                'country': movie.country.name,
                'running_time': movie.running_time,
                'release_date': movie.release_date.strftime('%Y-%m-%d'),
                'director': movie.director,
                'rating': movie.rating.name,
                'image': movie.image,
                'summary': movie.summary,
                'audience_score': movie.audience_score,
                'netizen_score': movie.netizen_score,
                'reporter_critic_score': movie.reporter_critic_score,
                'actor': [data.actor.name for data in MovieActor.objects.filter(movie=movie)],
                'genre': [data.genre.name for data in MovieGenre.objects.filter(movie=movie)]
            }
            return JsonResponse({'message': 'Success', 'movie_data': result}, status=200)

        except Exception as e:
            return JsonResponse({'message': '{}'.format(e)}, status=500)
