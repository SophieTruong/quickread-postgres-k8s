# quickread-postgres-k8s

Source boilerplate: https://testdriven.io/blog/dockerizing-flask-with-postgres-gunicorn-and-nginx/
## Usage instruction

- `git clone https://github.com/SophieTruong/quickread-postgres-k8s.git`
- Use `.env.dev.sample`, `.env.prod.sample`, `.env.prod.db.sample` as guide and fill in your configs. 

### Local environment
- Set up virtual environment:

### Run test
In rootdir
    `python -m pytest services/flaskapp/tests --setup-show --cov=services/flaskapp/src`
### Development
- In root, run `docker compose up -d --build` to build and run the docker images. Then, run `docker compose exec web python manage.py create_db` to start the app and create db table
- To spin off the container, run `docker compose down -v`

### Production 
- In root, run `docker compose -f docker-compose.prod.yml up -d --build` to build and run the docker images. Then, run `docker compose -f docker-compose.prod.yml exec web python manage.py create_db` to start the app and create db table
- To spin off the container, run `docker compose -f docker-compose.prod.yml down -v`

