import scrapy
import json
from rustore.items import RustoreItem


class AppSpider(scrapy.Spider):
    name = "app"
    urls = []

    def parse(self, response):
        sitemap_links = response.xpath("//url").getall()
        filtered_links = [link for link in sitemap_links if 'https://apps.rustore.ru/app/' in link]

        for link in filtered_links:
            packageName = link.replace('https://apps.rustore.ru/app/', '')
            app_url = f"https://apps.rustore.ru/_next/data/sd-7mWtXf28eFs6SQ5gVh/app/" \
                      f"{packageName}.json?id=" \
                      f"{packageName}"
            yield scrapy.Request(app_url, callback=self.parse_app)

    def parse(self, response):
        item = RustoreItem()
        data = json.loads(response.text)
        app_detail = data["pageProps"]["dehydratedState"]["queries"][0]["state"]["data"]["body"]
        item["dataUpdatedAt"] = data["pageProps"]["dehydratedState"]["queries"][0]["state"]["dataUpdatedAt"]
        item["status"] = data["pageProps"]["dehydratedState"]["queries"][0]["state"]["status"]
        rating = data["pageProps"]["dehydratedState"]["queries"][1]["state"]["data"]["body"]
        reviews = data["pageProps"]["dehydratedState"]["queries"][2]["state"]["data"]["body"]

        item["appId"] = app_detail["appId"]
        item["packageName"] = app_detail["packageName"]
        item["appName"] = app_detail["appName"]
        item["category"] = app_detail["category"]
        categories = app_detail["categories"]
        item["count_categories"] = len(categories)
        item["categories"] = ', '.join(categories)
        item["companyName"] = app_detail["companyName"]
        item["ownerVkId"] = app_detail["ownerVkId"]
        item["shortDescription"] = app_detail["shortDescription"].replace("\n", ' ')
        item["fullDescription"] = app_detail["fullDescription"].replace("\n", ' ')
        item["moderInfo"] = app_detail["moderInfo"]
        item["companyStatus"] = app_detail["companyStatus"]
        item["ageLegal"] = app_detail["ageLegal"]
        item["fileSize"] = app_detail["fileSize"]
        item["versionName"] = app_detail["versionName"]
        item["versionCode"] = app_detail["versionCode"]
        item["minSdkVersion"] = app_detail["minSdkVersion"]
        item["targetSdkVersion"] = app_detail["targetSdkVersion"]
        item["maxSdkVersion"] = app_detail["maxSdkVersion"]
        item["whatsNew"] = app_detail["whatsNew"].replace("\n", ' ')
        item["iconUrl"] = app_detail["iconUrl"]
        fileUrls = app_detail["fileUrls"]
        item["count_images"] = len(fileUrls)
        item["appType"] = app_detail["appType"]
        item["website"] = app_detail["website"]
        item["signature"] = app_detail["signature"]
        privacyDataCategories = app_detail["privacyDataCategories"]
        item["countprivacyDataCategories"] = len(privacyDataCategories)
        item["adaptedToTablets"] = app_detail["adaptedToTablets"]
        item["companyLegalForm"] = app_detail["companyLegalForm"]
        item["downloads"] = app_detail["downloads"]
        item["purchased"] = app_detail["purchased"]
        item["price"] = app_detail["price"]
        item["appVerUpdatedAt"] = app_detail["appVerUpdatedAt"]
        item["inAppUpdatePriority"] = app_detail["inAppUpdatePriority"]
        item["banner"] = app_detail["banner"]
        item["aggregatorInfo"] = app_detail["aggregatorInfo"]
        item["video"] = app_detail["video"]

        item["amountFive"] = rating["ratings"]["amountFive"]
        item["amountFour"] = rating["ratings"]["amountFour"]
        item["amountThree"] = rating["ratings"]["amountThree"]
        item["amountTwo"] = rating["ratings"]["amountTwo"]
        item["amountOne"] = rating["ratings"]["amountOne"]
        item["averageUserRating"] = rating["averageUserRating"]
        item["totalRatings"] = rating["totalRatings"]

        item["total_reviews"] = reviews["totalElements"]
        yield item