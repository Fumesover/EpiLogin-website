ssh root@parou.eu "cd /var/www/epilogin.parou.eu; docker-compose exec epiloginweb-db pg_dump postgres -U postgres" | docker exec -i $(docker run --rm -d -p 5432:5432 postgres) psql -U postgres
