# News_Recommend_System
AWS, MongoDB, Kafka, RPC, Redis

**System diagram**

![news](https://github.com/XinxinTang/News_Recommendation_System-AWS/blob/master/Images/Screen%20Shot%202018-04-05%20at%203.10.50%20PM.png)

**Program Description** <br>
1. The system monitored news source. Once fresh news published, system scraped the body text and computed similarity between fresh news and news stored in MongoDB using algorithm TF-IDF. After that, System stored distinct news in MongoDB. <br>
2. Here we built a CNN model for classification. We took some data from MongoDB as training set to train CNN model. 
3. Made a classification for all pieces of news using trained CNN model
4. Recommended some news which has same category with the news user clicked. 
This is the whole recommendation system! 

## Get started <br>
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


