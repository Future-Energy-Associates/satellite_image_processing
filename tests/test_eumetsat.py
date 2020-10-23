import os
import pytest
import dotenv

def test_load_env_vars(env_var_keys=['user_key', 'user_secret', 'slack_id', 'slack_webhook_url']):
    dotenv.load_dotenv('../.env')
    
    for env_var_key in env_var_keys:
        env_var = os.environ.get(env_var_key)
        
        assert env_var is not None, f'The {env_var_key} was not loaded succesfully'
