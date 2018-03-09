# News_Recommend_System
=
AWS, MongoDB, Kafka, RPC, Redis


System diagram:

![shiyanlou logo](https://github.com/XinxinTang/News_Recommendation_System-AWS/blob/master/Images/News-kafka.png)

## Get started <br>
Please install Big data tools: MongoDB, Kafka, Redis <br>
Please connect to AWS

1. Run MongoDB locally <br>
'''./mongod''' <br>
2. Start data generator <br>
You can run python code file 'monitor.py, fetcher.py, deduper.py' seperately, or
run 'news_pipeline_launcher.sh' file to start them all.

>3. Run 'service.py, recommendation_service.py, server.py, click_log_processor.py' to start all services <br>

4. Go to webserver/server 'npm install'  'npm start' to start server <br>

5. Go to webserver/client 'npm run build' to create build folder then 'npm start'. It will be jumped to the login page immediately, sign up first and log in. Congrats! We are done so far! <br>


