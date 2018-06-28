# News_Recommend_System
**Key words:** AWS, MongoDB, Kafka, RPC, Redis, Real-time Recommendation System

## System Diagram


![news](https://github.com/XinxinTang/News_Recommendation_System-AWS/blob/master/Images/Screen%20Shot%202018-04-05%20at%203.10.50%20PM.png)

## Program Description  
There are two main components in this project: Data collection and storage and Full-stack recommendation service.

### 1. Data collection and storage  
![Imgur](https://i.imgur.com/gMWeFPA.png)
1.1 Monitored news source based on News APIs. Once latest news published, monitor will check repeatness based on encoded title-**Digest**. Then this system sent a list of key/value pair to Kafka Broker  
```
Kafka Queue Keyset: Source, Author, Title(md5), url, urlToImage, PublishedAt, Digest
```  
1.2 Fetched news content based on url and NewsPaper API. Add content in message array.
```
Kafka Queue Keyset: Source, Author, Title(md5), url, urlToImage, PublishedAt, Digest, Text
```  
1.3 Eliminated repeated news based on TF-IDF algorithm, and add class for each news based on Deep Learning CNN model. Storing these news into MongoDB eventually. 
```
Kafka Queue Keyset: Source, Author, Title(md5), url, urlToImage, PublishedAt, Digest, Text, Class
MongoDB: Source, Author, Title(md5), url, urlToImage, PublishedAt, Digest, Text, Class
```  
**Notes:**
To classify automatically, we executed first two steps to collect a lot of news. Extracting news title and manual class label as Deep Learning training set. 


### 2. Full-Stack recommendation service
![Imgur](https://i.imgur.com/H1WJs1a.png)
2.1 Collected User's click event includes UserID, NewsID and timestamp.  
2.2 Updated **User Preference Model** of each class based on Time Decay method:
```
{Clicked: (1-alpha)*old_p + alpha; non-clicked: (1-alpha)*old_p}  
```  
2.3 Sent the target class news from MongoDB to Front-end Website for viewing based on **User Preference Class**  


## Get started  
Please install Big data tools: MongoDB, Kafka, Redis <br>
Please connect to AWS

1. Run MongoDB locally <br>
>./mongod <br>
2. Start data generator <br>
You can run the following python code file seperately, or run 'news_pipeline_launcher.sh' file to start them all <br>
> monitor.py, fetcher.py, deduper.py

3. Run the following python code files to start all services <br>
>service.py, recommendation_service.py, server.py, click_log_processor.py

4. Go to webserver/server 'npm install'  'npm start' to start server <br>

5. Go to webserver/client 'npm run build' to create build folder then 'npm start'. It will be jumped to the login page immediately, sign up first and log in. Congrats! We are done so far! <br>

6. go to login page
