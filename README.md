### 영화 정보 api
- 영화 list
- 영화 상세페이지 (CRUD)
- content_type이 json이 아닌 경우 406 error가 발생하는 데코레이터를 decorator.py에 작성하여 api에 적용
- unit test

---

파일 설치 후 제일 먼저 terminal에서 가상환경 설치 & 실행 후 해당 명령어를 실행합니다.

프로젝트에 필요한 패키지를 한번에 설치해주는 명령어입니다.

`$ pip install -r requirements.txt`

해당 프로젝트의 모델을 데이터베이스에 적용시켜주는 명령어입니다.

`$ python manage.py migrate`

unit test를 작성하였으며 테스트 하는 명령어는 다음과 같습니다.

`$ python manage.py test`

---

영화 리스트
GET /movies

영화 상세페이지 보기
GET /movies/{movie_id}

영화 정보 생성하기
POST /movies

영화 상세페이지 수정하기
PUT /movies

영화 정보 삭제하기
DELETE /movies

