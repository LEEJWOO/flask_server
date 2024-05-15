from pocketbase import PocketBase

pb = PocketBase('http://127.0.0.1:8090')
# titleID는 실제 DB에서 쓰이지 않음!! 추가 XXXX, DB 임의 변경 절대 XX, 다른 코드에 오류 발생할 가능성 많음!!

def get_webtoons():
    records = pb.collection('webtoons').get_full_list()

    webtoons = []
    for record in records:
        webtoon = {
            "id": record.id,
            "collectionId": record.collection_id,
            "collectionName": record.collection_name,
            "title": record.title,
            "url": record.url,
            "label": record.label,
            "last_ep": record.last_ep,
            "stars": record.stars,
            "total_count": record.total_count
        }
        webtoons.append(webtoon)

    return webtoons


def get_all_webtoons():
    query_params = {
        "expand": "label,stars,total_count"
    }

    records = pb.collection('webtoons').get_list(1, 100, query_params)

    webtoons = []

    for record in records.items:
        labels = []
        if 'label' in record.expand and record.expand['label']:
            for label_record in record.expand['label']:
                label = {
                    "id": label_record.id,
                    "positive_count": label_record.positive_count,
                    "positive_summary": label_record.positive_summary,
                }
                labels.append(label)

        if 'stars' in record.expand and record.expand['stars']:
            stars = {
                "id": record.expand['stars'].id,
                "star_list": record.expand['stars'].star_list
            }
        else:
            stars = None
            
        if 'total_count' in record.expand and record.expand['total_count']:
            total_count = {
                "id": record.expand['total_count'].id,
                "total_p": record.expand['total_count'].total_p,
                "total_n": record.expand['total_count'].total_n
            }
        else:
            total_count = None

        webtoon = {
            "id": record.id,
            "collectionId": record.collection_id,
            "collectionName": record.collection_name,
            "title": record.title,
            "url": record.url,
            "last_ep": record.last_ep,
            "label": labels,
            "stars": stars,
            "total_count": total_count
        }

        webtoons.append(webtoon)

    return webtoons

# 확장 콜렉션까지 출력하도록 수정
# 실행 확인 완료
def get_one_webtoons(tit):
    query_params = {
        "expand": "label,stars,total_count"
    }
    title = tit
    recordID = ""
    toon_list = get_all_webtoons()
    for toon in toon_list:
        if toon['title'] == title:
            recordID = toon['id']
            break

    record = pb.collection('webtoons').get_one(recordID, query_params)

    labels = []
    if 'label' in record.expand and record.expand['label']:
        for label_record in record.expand['label']:
            label = {
                "id": label_record.id,
                "positive_count": label_record.positive_count,
                "positive_summary": label_record.positive_summary,
            }
            labels.append(label)

    if 'stars' in record.expand and record.expand['stars']:
        stars = {
            "id": record.expand['stars'].id,
            "star_list": record.expand['stars'].star_list
        }
    else:
        stars = None

    if 'total_count' in record.expand and record.expand['total_count']:
        total_count = {
            "id": record.expand['total_count'].id,
            "total_p": record.expand['total_count'].total_p,
            "total_n": record.expand['total_count'].total_n
        }
    else:
        total_count = None

    webtoon = {
        "id": record.id,
        "collectionId": record.collection_id,
        "collectionName": record.collection_name,
        "title": record.title,
        "url": record.url,
        "last_ep": record.last_ep,
        "label": labels,
        "stars": stars,
        "total_count": total_count
    }

    return webtoon

def create_webtoon(title, url):
    data = {
        "title": title,
        "url": url
    }
    record = pb.collection('webtoons').create(data)
    return record.title

def create_label(label, p_count, p_summary):
    data = {
        "label": label,
        "positive_count": p_count,
        "positive_summary": p_summary,
    }
    record = pb.collection('label_webtoon').create(data)
    return record.label

# 이 코드 사용해서 별점 레코드 생성하고, star_list가 아닌 id값 받아오기
def create_stars(s_list):
    data = {
        "star_list": s_list
    }
    record = pb.collection('stars_webtoon').create(data)
    return record.id
def update_stars_webtoon(webtoon_id, star_id):
    data = {
        "stars": star_id,
    }
    record = pb.collection('webtoons').update(webtoon_id, data)
    print(record.__dict__)
    return record.stars

#TODO 하드코딩된 값들 교체해야 함
def update_label_webtoon():
    data = {
        "title": "트리거",
        "label": [
            "3nwlsk6lwo5km64"
        ],
        "stars": "pulvo96v85z2zix",
    }
    record = pb.collection('webtoons').update('kskm56pt3jkjjp6', data)
    print(record.__dict__)
    return record.label

#TODO 하드코딩된 값들 교체해야 함
def update_stars_webtoon():
    data = {
        "stars": "pulvo96v85z2zix",
    }
    record = pb.collection('webtoons').update('kskm56pt3jkjjp6', data)
    print(record.__dict__)
    return record.star


def delete_webtoon(id):
    pb.collection('webtoons').delete(id)
    return "delete 성공"
def update_webtoon_stars(titleId, stars_data):
    data = {"stars": stars_data}
    record = pb.collection('webtoons').update(titleId, data)
    return record

def update_webtoon_label(titleId, label_data):
    data = {"label": label_data}
    record = pb.collection('webtoons').update(titleId, data)
    return record

#0513 app.py save_comments_data 때문에 필요
def create_comments(param): #미완
    return None
