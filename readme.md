### 프로젝트 실행
  - project_app이 아닌 루트(DS-SECTION3-PROJECT)에서 실행한다.
  - FLASK_APP=project_app flask run


### 프로젝트 구조

1. 루트 직하위 directory는 data, pickles, project_app로 되어있으며, 프로젝트 앱은 project_app디렉토리에 다 모여있다.
2. project_app
   1) init에서 db연결하고 db 내용이 없으면 캐글로부터 파일을 불러온다. 캐글로부터 csv파일을 불러오는 함수와 csv파일을 이용해 db에 저장하는 함수를 짠다. 해당 함수는 modules라는 디렉토리에 downloader.py로 저장한다.
   2) pickle로부터 모델을 불러온다. 없으면 모델을 생성하며 다소 시간이 걸린다.
   3) 불러온 모델로 인덱스 페이지에서 제출한 값을 이용해 뇌졸중 확률을 얻는다.


### 데이터 랭글링
- bmi 결측치가 5110개 중에 201개로 4%에 가까운 수치였기 때문에 어쩔 수 없이 항목에 포함시키고자 평균치로 적용했음.

### 대시보드
- 아래와 같이 도커로 실행한 경우로 가정하여 제작되었습니다.
  - docker run -d -p 3000:3000 --name metabase metabase/metabase
- stroke ratio => CountIf([Stroke] = 1) / (CountIf([Stroke] = 1) + CountIf([Stroke] = 0))


- 기본 요구 사항
  - 캐글 토큰을 필요로 합니다. 자세한 사항은 https://www.kaggle.com/docs/api#getting-started-installation-&-authentication을 참고하세요.
  - postgreDB가 설치가 되어 있어야 하며, 'postgres' database가 기본적으로 생성이 되어 있어야 합니다.

- 추가로 install이 필요한 라이브러리
  - kaggle
  - python-dotenv
  - psycopg2
  - sqlalchemy
  - scikit-learn
  - xgboost
  - eli5