import requests, json, datetime, pymongo

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["pagespeed"]
scores_col = db["scores"]
urls_col = db["urls"]

for url_doc in urls_col.find():
    url = url_doc['url']
    page = url_doc['page_name']
    
    for platform in ['desktop', 'mobile']:
        result = json.loads(requests.get("https://www.googleapis.com/pagespeedonline/v5/runPagespeed?strategy=" + platform + "&url=" + url).content)
        score = result["lighthouseResult"]["categories"]["performance"]["score"]
        timestamp = datetime.datetime.strptime(result["lighthouseResult"]["fetchTime"], '%Y-%m-%dT%H:%M:%S.%fZ')
        reports.append({ "page": page, "platform": platform, "score": score, "timestamp": timestamp })
scors_col.insert_many(reports)