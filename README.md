# django-ecommerce

### setup

`python manage.py migrate --settings=dripshop.settings.dev`
`python manage.py runserver --settings=dripshop.settings.dev`

install redis and run on port `localhost:6739`

start the celery worker
`celery -A dripshop worker --loglevel=info`

start the celery-beat-scheduler
`celery -A dripshop beat --loglevel=info`


`celery -A myapp.celeryapp worker --loglevel=info -P eventlet`