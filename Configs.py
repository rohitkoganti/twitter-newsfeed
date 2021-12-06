from decouple import config


class Var:
    # Telegram's API ID
    API_ID = config("API_ID", '13365810')
    # Telegram's API HASH
    API_HASH = config("API_HASH", 'dc244bc5d3696c478a54f74d666bec20')
    # Telegram Bot's token
    BOT_TOKEN = config("BOT_TOKEN", '5048252615:AAG0zqe6jcKeFSNZHwWZWeBdJS10maU0hMs')

    # Twitter Vars
    CONSUMER_KEY = config("CONSUMER_KEY", 'PePMO0Yj4megfEMyWp4b5lNUW')
    CONSUMER_SECRET = config("CONSUMER_SECRET", 'fe9xex9IVY3dqRNXFGFfckRE8Jy64COZim1V2e3ViZN1x5nks4')
    ACCESS_TOKEN = config("ACCESS_TOKEN", '142013277-aVxNzMICaWDWp9IIVFdadPPwHJ7DBEknh3zVgjK0')
    ACCESS_TOKEN_SECRET = config("ACCESS_TOKEN_SECRET", 'GUNxnAWoT5urOoOBQ1UVDcF8v3GW4hIW9rH72P97vy3aP')

    # Telegram Chat id(s), where to send Tweets
    TO_CHAT: str = config("TO_CHAT", '-1001654428545')

    # Username of Twitter User, whose Tweets should be tracked
    # and posted to chat filled in TO_CHAT.
    TRACK_USERS = config("TRACK_USERS", '@DDNewslive')
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
    TAKE_REPLIES = config("TAKE_REPLIES", default=False, cast=bool)
    # Whether to Take Retweets or not.
    TAKE_RETWEETS = config("TAKE_RETWEETS", default=False, cast=bool)
    # Whether to take replies on post of user filled in TRACK_USERS.
    TAKE_OTHERS_REPLY = config("TAKE_OTHERS_REPLY", default=False, cast=bool)

    # An Addition word checking filters.
    MUST_INCLUDE = config("MUST_INCLUDE", default=None)
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
