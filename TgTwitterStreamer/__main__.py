# Telegram - Twitter - Bot
# Github.com/New-dev0/TgTwitterStreamer
# GNU General Public License v3.0

import re
import asyncio
import aiohttp
from telethon.events import NewMessage, CallbackQuery
from telethon.tl.custom import Button
from tweepy.asynchronous import AsyncStream
from tweepy.errors import Unauthorized

from . import Twitter, Client, REPO_LINK, Var, LOGGER, mycol


LOGGER.info("<<--- Setting Up Bot ! --->>")

TRACK_IDS = None
TRACK_WORDS = None
CACHE_USERNAME = []

if Var.TRACK_USERS:
    TRACK_IDS = []
    for username in Var.TRACK_USERS.split(" "):
        try:
            user = Twitter.get_user(screen_name=username)._json
            TRACK_IDS.append(user["id_str"])
            LOGGER.info(
                f"<<--- Added {user['screen_name']}" +
                " to TRACK - LIST ! --->>"
            )
        except Unauthorized as er:
            LOGGER.exception(er)
            exit()
        except Exception as e:
            LOGGER.exception(e)

if Var.TRACK_WORDS:
    TRACK_WORDS = Var.TRACK_WORDS.split(" | ")


class TgStreamer(AsyncStream):
    async def on_connect(self):
        LOGGER.info("<<<---||| Stream Connected |||--->>>")

    def get_urls(self, media):
        if not media:
            return []

        List = []

        for media in media:
            if media.get("video_info") and media["video_info"].get("variants"):
                link = media["video_info"]["variants"][0]["url"]
            elif media["type"] == "photo":
                link = media["media_url_https"]
            else:
                link = None
            if link and "tweet_video_thumb" not in link:
                List.append(link)
        return List

    async def on_status(self, status):
        tweet = status._json
        #LOGGER.info(tweet)
        user = tweet["user"]

        if (
            not Var.TRACK_WORDS
            and Var.TRACK_USERS
            and not Var.TAKE_OTHERS_REPLY
            and not user["id_str"] in TRACK_IDS
        ):
            return

        if not Var.TAKE_REPLIES and tweet["in_reply_to_status_id"]:
            return

        if not Var.TAKE_RETWEETS and tweet.get("retweeted_status"):
            return

        # Cache BOT Username
        try:
            bot_username = CACHE_USERNAME[0]
        except IndexError:
            bot_username = (await Client.get_me()).username
            CACHE_USERNAME.append(bot_username)

        pic, content, hashtags = [], "", ""
        _entities = tweet.get("entities", {})
        entities = _entities.get("media", [])
        extended_entities = tweet.get("extended_entities", {}).get("media")
        extended_tweet = (
            tweet.get("extended_tweet", {}).get("entities", {}).get("media")
        )
        all_urls = set()
        for media in (entities, extended_entities, extended_tweet):
            urls = self.get_urls(media)
            all_urls.update(set(urls))
        for pik in all_urls:
            pic.append(pik)
        if _entities and _entities.get("hashtags"):
            hashtags = "".join(f"#{a['text']} " for a in _entities["hashtags"])

        username = user["screen_name"]
        sender_url = "https://twitter.com/" + username
        TWEET_LINK = f"{sender_url}/status/{tweet['id']}"

        if "retweeted_status" in tweet and tweet["is_quote_status"] is True:
            content = 'RT @' + tweet.get("retweeted_status",{}).get("user",{}).get("screen_name") + ': ' + tweet.get("retweeted_status",{}).get("text") + '\n' + tweet.get("retweeted_status",{}).get("quoted_status_permalink",{}).get("expanded")
        elif "retweeted_status" in tweet:
            content = 'RT @' + tweet.get("retweeted_status",{}).get("user",{}).get("screen_name") + ': ' + (tweet.get("retweeted_status",{}).get("extended_tweet",{}).get("full_text") or tweet.get("retweeted_status",{}).get("text"))
        elif tweet["is_quote_status"] is True:
            content = 'QT @' + tweet.get("quoted_status",{}).get("user",{}).get("screen_name") + ': ' + tweet.get("text",{}) + '\n' + tweet.get("quoted_status_permalink",{}).get("expanded")
        else:
            content = tweet.get("extended_tweet", {}).get("full_text")

        if content and (len(content) < 1000):
            text = content
        else:
            text = tweet["text"]

        if Var.MUST_INCLUDE and Var.MUST_INCLUDE not in text:
            return

        if Var.MUST_EXCLUDE and Var.MUST_EXCLUDE in text:
            return

        spli = text.split()
        async with aiohttp.ClientSession() as ses:
            for on in spli:
                if "t.co/" in on:
                    link = "https://t.co/" + on.split("t.co/")[1] #Making sure the link to be decoded is legit
                    async with ses.get(link) as out:
                        text = text.replace(link, str(out.url))

        # Twitter Repeats Media Url in Text.
        # So, Its somewhere necessary to seperate out links.
        # to Get Pure Text.

        for word in text.split():
            if word.startswith("https://twitter.com"):
                spli_ = word.split("/")
                if len(spli_) >= 2 and spli_[-2] in ["photo", "video"]:
                    text = text.replace(word, "")

        final_text = Var.CUSTOM_TEXT.format(
            SENDER=user["name"],
            SENDER_USERNAME="@" + username,
            TWEET_TEXT=text,
            TWEET_LINK=TWEET_LINK,
            SENDER_PROFILE=sender_url,
            SENDER_PROFILE_IMG_URL=user["profile_image_url_https"],
            _REPO_LINK=REPO_LINK,
            HASHTAGS=hashtags,
            BOT_USERNAME=bot_username,
        )
        if pic == []:
            pic = None

        button = None
        if not Var.DISABLE_BUTTON:
            button = Button.url(text=Var.BUTTON_TITLE, url=TWEET_LINK)

        is_pic_alone = bool(not pic or len(pic) == 1)
        _photos = pic[0] if (pic and is_pic_alone) else pic
        if _photos == []:
            _photos = None

        for chat in Var.TO_CHAT:
            try:
                message1 = await Client.send_message(
                    chat,
                    final_text if (is_pic_alone or Var.DISABLE_BUTTON) else None,
                    link_preview=False,
                    file=_photos,
                    buttons=button,
                )
                LOGGER.info(message1)
                if not is_pic_alone and final_text and button:
                    message2 = await Client.send_message(
                        chat, final_text, link_preview=False, buttons=button
                    )
                    LOGGER.info(message2)
            except Exception as er:
                LOGGER.exception(er)

        if Var.AUTO_LIKE:
            try:
                Twitter.create_favorite(id=tweet["id"])
            except Exception as er:
                LOGGER.exception(er)
        if Var.AUTO_RETWEET:
            try:
                Twitter.retweet(id=tweet["id"])
            except Exception as er:
                LOGGER.exception(er)
        # Saving the tweet in the db
        ids = []
        if "message1" in locals():
            if isinstance(message1, list):
                for m in message1:
                    ids.append(m.id)
            else:
                ids.append(message1.id)

        if "message2" in locals():
            ids.append(message2.id)

        save_tweet = {"tweet_text": text,
                    "tweet_link": TWEET_LINK,
                    "message_ids": ids
                    }
        LOGGER.info(save_tweet)
        mycol.insert_one(save_tweet)

    async def on_delete(self, status_id, user_id):
        #Search for the tweet with a tweet link that matches the status_id and user_id
        #print(status_id, user_id)
        sender_url = "https://twitter.com/" + Var.TRACK_USERS.split(" ")[0]
        TWEET_LINK = f"{sender_url}/status/{status_id}"
        print(TWEET_LINK)

        #search for tweet link in db
        match = mycol.find_one({'tweet_link':TWEET_LINK})
        LOGGER.info(match)

        #get associated message ids
        ids = []
        if match is not None:
            ids = match['message_ids']

        #delete messages iteratively. Only one chat is taken here, may add more.
        for id in ids:
            try:
                await Client.delete_messages(Var.TO_CHAT[0], str(id))
            except Exception as er:
                LOGGER.exception(er)

    async def on_request_error(self, status_code):
        LOGGER.error(f"Stream Encountered HTTP Error: {status_code}")
        if status_code == 420:
            # Tweepy already makes Connection sleep for 1 minute on 420 Error.
            # So, Here making it sleep for more 10 seconds.
            await asyncio.sleep(10)
        LOGGER.info(
            "Refer https://developer.twitter.com/ja/docs/basics" +
            "/response-codes to know about error code."
        )

    async def on_connection_error(self):
        LOGGER.info("<<---|| Connection Error ||--->>")


async def start_message(event):
    await event.reply(
        Var.START_MESSAGE,
        file=Var.START_MEDIA,
        buttons=[
            [Button.inline("Hello Sir, i'm Alive", data="ok")],
            [
                Button.url(
                    "Source",
                    url=REPO_LINK,
                ),
                Button.url("Support Group", url="t.me/FutureCodesChat"),
            ],
        ],
    )


async def callback_query(event):
    await event.answer("I'm Alive , No Need to click button..")


# For people, deploying multiple apps on one bot. (including "me")
if not Var.DISABLE_START:
    Client.add_event_handler(
        start_message,
        NewMessage(pattern="^/start$")
    )
    Client.add_event_handler(
        callback_query,
        CallbackQuery(data=re.compile("ok"))
    )

if __name__ == "__main__":
    Stream = TgStreamer(
        Var.CONSUMER_KEY, Var.CONSUMER_SECRET,
        Var.ACCESS_TOKEN, Var.ACCESS_TOKEN_SECRET
    )
    Stream.filter(
        follow=TRACK_IDS,
        track=TRACK_WORDS,
        filter_level=Var.FILTER_LEVEL,
        languages=Var.LANGUAGES,
    )

    with Client:
        Client.run_until_disconnected()  # Running Client
