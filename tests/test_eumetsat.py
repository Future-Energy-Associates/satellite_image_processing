import os
import pytest
import dotenv

def test_load_env_vars():
    print(os.listdir())
    dotenv.load_dotenv('../.env')

    user_key = os.environ.get('user_key')
    user_secret = os.environ.get('user_secret')
    slack_id = os.environ.get('slack_id')
    slack_webhook_url = os.environ.get('slack_webhook_url')

    assert user_key is not None
    print(slack_id)
