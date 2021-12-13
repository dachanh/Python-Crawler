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

I decide the database like the diagram above, Because the input of client is the url and level , in the url of website have so much href both the href on internal website and href of external website. I just forcus crawl the internal url because If i forcus the external url , the infomation crawl maybe so much information.

<b>The architecture</b>: client -> nginx -> gunicorn -> flask(python)
Some consider I implement in the project:
- I design the crawler like BFS algorithm and just crawl continue the internal href.
- Design safe thread to avoid the GIL in python, every thread request crawl the URL I just make sure don't happen request don't success so I design retry pattern and retry 3 times for every request failded. you can check the source code here : ./Challenge2/crawler/app/crawler.py
- Make every url don't crawl more one times, I check save the url into the set datatype to make sure just every url is unique.
- Every deploy the server will generator the debug log and its name is crawler.log
- the Nginx I design the custom log conatiner information about uri , request , agent ...

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

   
Furure work:
      There is simple crawler so more inconvenience, below is some the idea to upgrade the application:
   - Deploy the application use docker 
   - Distributed crawl to achieve high performance
   - Redundant content , use hasher or checksum help dectect deduplication
   - Cache DNS Resolver If many request from client go to the website will blocked 
 
 Above all my implement to complete the asignment, Any inconvenient please contact me with the email: lamnguyent7@gmail.com
