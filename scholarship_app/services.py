import requests
import hashlib
from django.core.cache import cache
from django.conf import settings


# def search_scholarships(query):
#     cache_key = "sch_" + hashlib.md5(query.encode()).hexdigest()
#     cached = cache.get(cache_key)
#     if cached:
#         return cached

#     headers = {"X-API-KEY": settings.SERPER_API_KEY}
#     payload = {
#         "q": f"{query} بورسیه",
#         "num": 10,
#         "gl": "ir",
#         "hl": "fa",
#     }

#     try:
#         res = requests.post(
#             "https://google.serper.dev/search",
#             json=payload,
#             headers=headers,
#             timeout=5
#         )
#         res.raise_for_status()
#         results = parse_results(res.json())
#         cache.set(cache_key, results, timeout=60 * 60 * 24)
#         return results
#     except Exception:
#         return []


# def parse_results(data):
#     results = []
#     for item in data.get("organic", []):
#         results.append({
#             "title": item.get("title", ""),
#             "description": item.get("snippet", ""),
#             "link": item.get("link", ""),
#             "source": item.get("displayLink", ""),
#             "country": "",
#             "level": "",
#             "deadline": "",
#         })
#     return results


# def get_popular_scholarships():
#     queries = ["بورسیه آلمان", "بورسیه کانادا", "بورسیه دکترا"]
#     results = []
#     for q in queries:
#         results.extend(search_scholarships(q)[:2])
#     return results[:6]



import requests
import hashlib
from django.core.cache import cache
from django.conf import settings


def parse_results(data):
    results = []
    for item in data.get("organic", []):
        results.append({
            "title": item.get("title", ""),
            "description": item.get("snippet", ""),
            "link": item.get("link", ""),
            "source": item.get("displayLink", ""),
            "country": "",
            "level": "",
            "deadline": "",
        })
    return results


def search_scholarships(query):
    cache_key = "sch_" + hashlib.md5(query.encode()).hexdigest()
    cached = cache.get(cache_key)
    if cached:
        return cached

    headers = {"X-API-KEY": settings.SERPER_API_KEY}
    payload = {
        "q": f"{query} بورسیه",
        "num": 10,
        "gl": "ir",
        "hl": "fa",
    }

    try:
        res = requests.post(
            "https://google.serper.dev/search",
            json=payload,
            headers=headers,
            timeout=5
        )
        results = parse_results(res.json())
        cache.set(cache_key, results, timeout=60 * 60 * 24)
        return results
    except Exception as e:
        return []


def get_popular_scholarships():
    queries = ["بورسیه آلمان", "بورسیه کانادا", "بورسیه دکترا"]
    results = []
    for q in queries:
        results.extend(search_scholarships(q)[:2])
    return results[:6]