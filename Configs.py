from decouple import config


class Var:
    # Telegram's API ID
    API_ID = config("API_ID", '13365810')
    # Telegram's API HASH
    API_HASH = config("API_HASH", 'dc244bc5d3696c478a54f74d666bec20')
    # Telegram Bot's token - In this case the bot "Twitter Streamer"
    BOT_TOKEN = config("BOT_TOKEN", '5077846941:AAGbikC6RnuqS1kV7KTmxzX3v1CQmfNvp5M')

    # Twitter Vars
    CONSUMER_KEY = config("CONSUMER_KEY", 'KE3EWi6xH3h3644zJwEF4kktZ')
    CONSUMER_SECRET = config("CONSUMER_SECRET", 'GKBjGqfBUReA7OcmviSH2HhgzmBbZeFU6YnPum5dyBDDeLVhsA')
    ACCESS_TOKEN = config("ACCESS_TOKEN", '142013277-TFqMKfTs34zy46NdnEvuW1KinhtQmKvnt59I2qVD')
    ACCESS_TOKEN_SECRET = config("ACCESS_TOKEN_SECRET", 'yexQY5bswpuMsoCv1YqowaksaS2o9r37QlmCklj7ZKIzK')

    # Telegram Chat id(s), where to send Tweets
    TO_CHAT: str = config("TO_CHAT", '-1001799980938') #'-1001670978742')
    #TO_CHAT: str = config("TO_CHAT", '-1001670978742')

    # Username of Twitter User, whose Tweets should be tracked
    # and posted to chat filled in TO_CHAT.
    TRACK_USERS = config("TRACK_USERS", '@the_hindu @DDNewslive @htTweets @timesofindia @ANI @PTI_News @IndianExpress @ndtv @ndtvfeed @airnewsalerts @IndiaTodayFLASH @IndiaToday @DeccanHerald @indiacom @ians_india @narendramodi @rashtrapatibhvn @PMOIndia')
    TRACK_IMP = config("TRACK_IMP", ['narendramodi', 'rashtrapatibhvn', 'PMOIndia'])
    # TRACK_WORDS: To filter Tweets by word
    # Should be seperated by "|"
    TRACK_WORDS = config("TRACK_WORDS", None)

    # Custom Text format to be used, while sending Tweets.
    CUSTOM_TEXT = config("CUSTOM_TEXT", None)
    # Text to Display on Button, Attached to Message Posted on Telegram.
    BUTTON_TITLE = config("BUTTON_TITLE", "View on Twitter🔗")
    # Set DISABLE_BUTTON to True, to disable that Button.
    DISABLE_BUTTON = config("DISABLE_BUTTON", default=False, cast=bool)

    # Media Url, to be send with '/start' message.
    START_MEDIA = config("START_MEDIA", "TgTwitterStreamer/assets/START.webp")
    if START_MEDIA == "None":
        START_MEDIA = None
    # Caption/text of '/start' message.
    START_MESSAGE = config("START_MESSAGE", None)
    DISABLE_START = config("DISABLE_START", default=False, cast=bool)

    # Whether should take messages, which are reply to other post.
    TAKE_REPLIES = config("TAKE_REPLIES", True, cast=bool)
    # Whether to Take Retweets or not.
    TAKE_RETWEETS = config("TAKE_RETWEETS", True, cast=bool)
    # Whether to take replies on post of user filled in TRACK_USERS.
    TAKE_OTHERS_REPLY = config("TAKE_OTHERS_REPLY", default=False, cast=bool)

    # An Addition word checking filters.
    MUST_INCLUDE = config("MUST_INCLUDE", ['Venkaiah Naidu', 'Vice President of India', 'VPSecretariat', 'passes away', 'passing away', 'passed away', 'accident', 'derail', 'capsize', 'turned turtle', 'mishap', 'demise', 'expire', 'injured', 'massive fire', 'fire incident' ])
    MUST_EXCLUDE = config("MUST_EXCLUDE", default=None)

    # Automations
    AUTO_LIKE = config("AUTO_LIKE", default=False, cast=bool)
    AUTO_RETWEET = config("AUTO_RETWEET", default=False, cast=bool)

    _filter_level = None
    # There can be Wide Range of Tweets.
    if TRACK_WORDS and not TRACK_USERS:
        _filter_level = "low"
    FILTER_LEVEL = config("FILTER_LEVEL", default=_filter_level)

    # Filter Language of Tweets
    LANGUAGES = config("LANGUAGES", default=None)
