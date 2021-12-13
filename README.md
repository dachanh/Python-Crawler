# Python Crawler
The requirements:
```
	Python3.6 
	Postgres
	Nginx
```
To convient , I install Postgres by docker 
```
docker run --name postgres-sql -e POSTGRES_PASSWORD=123456 -e POSTGRES_USER testdb -e POSTGRES_DB=crawlerDB -p 5432:5432 -d postgres 
```
 Database
 
![](image/diagram.png)

<b>Build</b>:
```
      pip install -r requirements.txt
      sudo cp Challenge2/crawler/default /etc/nginx/sites-enabled
      sudo systemctl restart nginx.service
      cd Challenge2/crawler/app
      ./migrate.sh
      ./run.sh
```
## API 
  - POST :  127.0.0.1:80/api/v1/crawler
  - Request
    - Content-type	: application/json
    - Body 
      ```
            {
	            "url": String,
	            "level": Int
            }
      ```
   - Response
     - Http code : 200
     - Body
     
			[
				{
					'url' : string,
					'is_internal_url': Boolean
				}
			]