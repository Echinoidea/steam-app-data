import json
import statistics


class SteamApp:
    app_id = ""
    name = ""
    developer = ""
    publisher = ""
    pos_reviews = 0
    neg_reviews = 0
    price = ""

    def __init__(self, app_id, name, developer, publisher, pos_reviews, neg_reviews, price):
        self.app_id = app_id
        self.name = name
        self.developer = developer
        self.publisher = publisher
        self.pos_reviews = pos_reviews
        self.neg_reviews = neg_reviews
        self.price = price

    def get_avg_pos_percentage(self):
        return self.pos_reviews / (self.pos_reviews + self.neg_reviews)


steam_app_list = []


def parse_json(filepath):
    global steam_app_list
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
            for i in data:
                #print(data[i]["name"])
                if data[i]["name"] is None:
                    continue
                else:
                    steam_app_list.append(SteamApp(data[i]["appid"], data[i]["name"], data[i]["developer"],
                                                   data[i]["publisher"], data[i]["positive"],
                                                   data[i]["negative"],
                                                   data[i]["price"]))
    except Exception as e:
        print("An error has occurred while trying to read {}! {}".format(filepath, e.args))
    finally:
        f.close()


def get_sample_positive_std_dev():
    pos_percentages = []
    for i in steam_app_list:
        pos_percentages.append(i.get_avg_pos_percentage())

    return statistics.stdev(pos_percentages)


parse_json("topsellers_all_top_1000.json")
print(len(steam_app_list))
print(get_sample_positive_std_dev())

sample_mean_a = 0
for i in steam_app_list:
    sample_mean_a += i.get_avg_pos_percentage()
sample_mean_a = sample_mean_a / len(steam_app_list)
print(f"Sample mean a = {sample_mean_a}")

std_dev_a = get_sample_positive_std_dev()
print(f"std dev a = {std_dev_a}")

steam_app_list.clear()

print("-----5000")
parse_json("topsellers_all_5000_minreview50.json")
print(len(steam_app_list))
print(get_sample_positive_std_dev())

sample_mean_a = 0
for i in steam_app_list:
    sample_mean_a += i.get_avg_pos_percentage()
sample_mean_a = sample_mean_a / len(steam_app_list)
print(f"Sample mean a = {sample_mean_a}")

std_dev_a = get_sample_positive_std_dev()
print(f"std dev a = {std_dev_a}")

steam_app_list.clear()
'''
parse_json("topsellers_indie_top_1000.json.json")
print(len(steam_app_list))
print(get_sample_positive_std_dev())

good_indies = []

for i in steam_app_list:
    if i.get_avg_pos_percentage() >= sample_mean_a + std_dev_a:
        #print(i.get_avg_pos_percentage())
        good_indies.append(i)

print(f"Number of indies that have a pos review % (x >= 1s): {len(good_indies)} ({len(good_indies)/len(steam_app_list)})")

# TODO: This is a mess. Make functions n shit
'''
'''
steam_app_list.clear()

parse_json("topsellers_publisher_top_100.json")
print(len(steam_app_list))
print(get_sample_positive_std_dev())
'''

'''
n = 100
Sample mean a = 0.879744411412807
std dev a = 0.09065978477285971

Indie:
n = 100
s = 0.08693414586676061

for n = 100, Number of indies that have a pos review % (x >= 1s): 16 (0.16)

--------------
All:
n = 995
Sample mean a = 0.8630939978011992
std dev a = 0.10129102561003499

Indie:
n = 997
std dev = 0.10057428425505265

for n = 1000, Number of indies that have a pos review % (x >= 1s): 106 (0.10631895687061184)
'''
