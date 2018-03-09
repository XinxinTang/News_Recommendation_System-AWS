from common import news_api_client as client


def test_basic():
    news = client.getNewsFromSource()
    '''
    author: News author
    title: News title
    description: Digest(key content)
    URL: News URL
    URLtoImage: image related to News
    publishedAt: publised time
    source: News Source
    '''
    print(news)
    assert len(news) > 0
    news = client.getNewsFromSource(sources=['bbc-news'])
    assert len(news) > 0
    print('test_basic passed!')


if __name__ == "__main__" :
    test_basic()
