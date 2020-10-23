import pytest
import dotenv

assert dotenv.load_dotenv('../.env), 'The environment variables were not loaded successfully'

user_key = os.environ.get('user_key')
user_secret = os.environ.get('user_secret')
slack_id = os.environ.get('slack_id')
slack_webhook_url = os.environ.get('slack_webhook_url')

print(slack_id)
