import requests
import re

# 替换为你的Bearer Token
BEARER_TOKEN = ""
# 替换为目标推文ID
TWEET_ID = "1892519800737350122"


def get_tweet_comments(tweet_id):
    url = "https://api.x.com/2/tweets/search/recent"
    headers = {
        "Authorization": f"Bearer {BEARER_TOKEN}"
    }

    params = {
        "query": f"conversation_id:{tweet_id} -is:retweet",
        "tweet.fields": "author_id,created_at,text",
        "max_results": 100

    }
    # params["next_token"]="b26v89c19zqg8o3frrcr1lz0ujt973tv5gzt0n4ch9ldp"

    comments = []

    while True:
        response = requests.get(url, headers=headers, params=params)
        if response.status_code != 200:
            print(f"请求失败: {response.status_code} - {response.text}")
            break

        data = response.json()
        comments.extend(data.get("data", []))

        # 检查是否有下一页（分页）
        next_token = data.get("meta", {}).get("next_token")
        if not next_token:
            break
        else:
            print(f"next_token:{next_token}")
        params["next_token"] = next_token

    return comments


def getETHAddressFromText(text):
    # 正则表达式匹配以太坊钱包地址
    pattern = r'0x[a-fA-F0-9]{40}'
    match = re.search(pattern, text)
    if match:
        return match.group()
    else:
        return None

def save_comment(file, index, comment):
    formatted_comment = f"{index}.[{comment['created_at']}] @{comment['author_id']}: {comment['text']}"
    file.write(formatted_comment + "\n")

def getCommentsAndSave():
    comments = get_tweet_comments(TWEET_ID)
    addresses = set()

    # 保存评论和钱包地址
    with open('comment.txt', 'a') as f_comment, open('address.txt', 'a') as f_addr:
        for idx, comment in enumerate(comments, 1):
            # 保存评论
            save_comment(f_comment, idx, comment)

            # 提取并保存地址
            addr = getETHAddressFromText(comment['text'])
            if addr and addr not in addresses:
                addresses.add(addr)
                f_addr.write(addr + "\n")



getCommentsAndSave()
