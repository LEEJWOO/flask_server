from pocketbase import PocketBase

pb = PocketBase('http://127.0.0.1:8090')


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
            "total_count": record.total_count,
            "label_summary": record.label_summary,
            "total_summary": record.total_summary
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
                    "label" : label_record.label,
                    "positive_count": label_record.positive_count,
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
            "total_count": total_count,
            "label_summary": record.label_summary,
            "total_summary": record.total_summary
        }

        webtoons.append(webtoon)

    return webtoons


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
                "label" : label_record.label,
                "positive_count": label_record.positive_count,
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
        "total_count": total_count,
        "label_summary": record.label_summary,
        "total_summary": record.total_summary
    }

    return webtoon


def create_webtoon(title, url):
    data = {
        "title": title,
        "url": url
    }
    record = pb.collection('webtoons').create(data)
    return record.id

def delete_webtoon(id):
    # webtoons 콜렉션에서 특정 ID를 가진 레코드 가져오기
    record = pb.collection('webtoons').get_one(id)
    pb.collection('webtoons').delete(id)

    # stars가 None이 아니고, 빈 값이 아닌 경우
    if record.stars:
        pb.collection('stars_webtoon').delete(record.stars)

    # label이 리스트 형태로 존재하고, 빈 리스트가 아닌 경우
    # label 리스트의 각 항목에 대해 삭제 작업 수행
    if record.label and isinstance(record.label, list) and record.label:
        for label_id in record.label:
            pb.collection('label_webtoon').delete(label_id)

    # total_count가 None이 아니고, 빈 값이 아닌 경우
    if record.total_count:
        pb.collection('count_webtoon').delete(record.total_count)

    return "delete 성공"

def delete_stars(id):
    pb.collection('stars_webtoon').delete(id)
    return "delete 성공"

def create_label(label, p_count):
    data = {
        "label": label,
        "positive_count": p_count,
    }
    record = pb.collection('label_webtoon').create(data)
    return record.id


def create_stars(s_list):
    data = {
        "star_list": s_list
    }
    record = pb.collection('stars_webtoon').create(data)
    return record.id

def create_count(p_count, n_count):
    data = {
        "total_p": p_count,
        "total_n": n_count
    }
    record = pb.collection('count_webtoon').create(data)
    return record.id

def update_label_webtoon(webtoon_id, label_ids):
    data = {
        "label": label_ids
    }
    record = pb.collection('webtoons').update(webtoon_id, data)
    return record.label


def update_stars_webtoon(webtoon_id, star_id, last_ep):
    data = {
        "stars": star_id,
        "last_ep": last_ep
    }
    record = pb.collection('webtoons').update(webtoon_id, data)
    return record.stars


def update_count_webtoon(webtoon_id, count_id):
    data = {
        "total_count": count_id,
    }
    record = pb.collection('webtoons').update(webtoon_id, data)
    return record.total_count

def update_summary_webtoon(webtoon_id, label_summary, total_summary):
    data = {
        "label_summary": label_summary,
        "total_summary": total_summary
    }
    record = pb.collection('webtoons').update(webtoon_id, data)
    return record.__dict__