# Observer_back
 
# Start
- upload docker -> postgres
- uvicorn main:app --host localhost --port 8000 --reload  -> start application 
- http://127.0.0.1:8000/docs -> Swagger documentation
- http://127.0.0.1:8000/redoc -> Redoc documentation
- http://127.0.0.1:8000/ -> template
- alembic revision --autogenerate -m "name" -> generation of migration
- alembic upgrade head -> implementation to DB 
- docker-compose up -> up REdis+Postgress
- docker-compose down -> shut REdis+Postgress