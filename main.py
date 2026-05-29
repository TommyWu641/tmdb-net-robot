import re

import requests
import csv
from lxml import html
MOVIE_LIST_FILE = "movie_list.csv"
URL_TOP20 = "https://www.themoviedb.org/movie/top-rated"
URL_BASE = "https://www.themoviedb.org/"
URL_TOP20_append = "https://www.themoviedb.org/discover/movie/items"


def get_movie_year(movie_years):
    movie_year = movie_years[0].strip() if movie_years else ''
    return movie_year.replace("(","").replace(")","")


def get_movie_publish_date(movie_dates):
    movie_date = movie_dates[0].strip() if movie_dates else ''
    return re.search(r"\d{4}/\d{2}/\d{2}", movie_date).group()


def get_movie_cost_times(movie_cost_times):
    cost_time = movie_cost_times[0].strip() if movie_cost_times else ''
    h_res = re.search(r"(\d)h", cost_time)
    m_res = re.search(r"(\d)m", cost_time)
    h = int(h_res.group(1)) if h_res else 0
    m = int(m_res.group(1)) if m_res else 0
    return h*60 + m

def get_movie_info(movie_info_url):
    # 1.发送请求，获取电影详情数据
    html_content = requests.get(movie_info_url)
    document = html.fromstring(html_content.text)

    # 2.解析数据，获取电影信息
    movie_names = document.xpath("//*[@id='original_header']/div[2]/section/div[1]/h2/a/text()")
    movie_years = document.xpath("//*[@id='original_header']/div[2]/section/div[1]/h2/span/text()")
    movie_dates = document.xpath("//*[@id='original_header']/div[2]/section/div[1]/div/span[@class='release']/text()")
    movie_tags = document.xpath("//*[@id='original_header']/div[2]/section/div[1]/div/span[@class='genres']/a/text()")
    movie_cost_times = document.xpath("//*[@id='original_header']/div[2]/section/div[1]/div/span[@class='runtime']/text()")
    movie_scores = document.xpath("//*[@id='consensus_pill']/div/div[1]/div/div/@data-percent")
    movie_languages = document.xpath("//*[@id='media_v4']/div/div/div[2]/div/section/div[1]/div/section[1]/p[3]/text()")
    movie_directors = document.xpath("//*[@id='original_header']/div[2]/section/div[3]/ol/li[1]/p[1]/a/text()")
    movie_authors = document.xpath("//*[@id='original_header']/div[2]/section/div[3]/ol/li[2]/p[1]/a/text()")
    movie_slogans = document.xpath("//*[@id='original_header']/div[2]/section/div[3]/h3[1]/text()")
    movie_descriptions = document.xpath("//*[@id='original_header']/div[2]/section/div[3]/div/p/text()")
    movie_info={
        "name": movie_names[0].strip() if movie_names else '',
        "year": get_movie_year(movie_years),
        "date": get_movie_publish_date(movie_dates),
        "tag": ",".join(movie_tags) if movie_tags else '',
        "cost_time": get_movie_cost_times(movie_cost_times),
        "score": movie_scores[0].strip() if movie_scores else '',
        "language": movie_languages[0].strip() if movie_languages else '',
        "director": ",".join(movie_directors) if movie_directors else '',
        "author": ",".join(movie_authors) if movie_authors else '',
        "slogan": movie_slogans[0].strip() if movie_slogans else '',
        "description": movie_descriptions[0].strip() if movie_descriptions else '',



    }
    print(movie_info)
    return movie_info
    # 3.返回电影详情

def save_all_movies(all_movies):
    with open(MOVIE_LIST_FILE, "w", encoding="utf-8", newline="") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=all_movies[0].keys())
        writer.writeheader()
        writer.writerows(all_movies)


def main():
    all_movies = []
    for page in range(1,6):
        # 1.发送请求，获取高分电影榜单数据
        if page == 1:
            html_content = requests.get(URL_TOP20)
        else:
            html_content = requests.post(URL_TOP20_append,
                                         f"air_date.gte=&air_date.lte=&certification=&certification_country=CN&debug=&first_air_date.gte=&first_air_date.lte=&include_adult=false&include_softcore=false&latest_ceremony.gte=&latest_ceremony.lte=&page={page}&primary_release_date.gte=&primary_release_date.lte=&region=&release_date.gte=&release_date.lte=2026-11-27&show_me=everything&sort_by=vote_average.desc&vote_average.gte=0&vote_average.lte=10&vote_count.gte=300&watch_region=CN&with_genres=&with_keywords=&with_networks=&with_origin_country=&with_original_language=&with_watch_monetization_types=&with_watch_providers=&with_release_type=&with_runtime.gte=0&with_runtime.lte=400"
                                         )

        document = html.fromstring(html_content.text)

        # 2.解析数据 获取电影列表
        movie_list = document.xpath(
            f"//*[@id='page_{page}']/div[@class='media-card-list contents w-full']/div[@class='media-list-results contents']/div")
        # 3.遍历电影列表，获取电影详情

        for movie in movie_list:
            movie_urls = movie.xpath("./div/div[1]/a/@href")
            if movie_urls:
                movie_info_url = URL_BASE + movie_urls[0]
                movie_info = get_movie_info(movie_info_url)
                all_movies.append(movie_info)

    # 4.保存数据，保存到csv文件中
    save_all_movies(all_movies)

if __name__ == '__main__':
    main()