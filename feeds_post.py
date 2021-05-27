from GoogleNews import GoogleNews
import pandas as pd
from pyshorteners import Shortener


googlenews = GoogleNews()
API_KEY = "8d3dc08c8a0d27a88e41a46b14b8c9106fc939c4"
API_USER = "cavatrendy"

s = Shortener(api_key=API_KEY)
def result_words(words):
    print("Analyzing " + words)
    googlenews.set_lang('en')
    googlenews.set_period('1d')
    googlenews.search(words)
    result = googlenews.result(sort=True)
    df_result = pd.DataFrame(result)
    return df_result

#create the df
food = result_words("Food Blockchain")
agriculture = result_words("Agriculture Blockchain")
#col of interest
col_list = ["title", "link"]
#df cleaning
df_diff = pd.concat([food,agriculture]).drop_duplicates(keep=False)
df_diff = df_diff[col_list]
#reduce the link size
link_to_short = []
for l in df_diff.get("link"):
    try:
        link_to_short.append(s.bitly.short(l))
        print(l)
    except:
        print("Not added " + l)
    # link_to_short.append(l)



# print(link_shorted)


