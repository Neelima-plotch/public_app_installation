
import os
from flask import Flask, request, redirect, session
import requests
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.urandom(24)

app_api_key = os.environ.get('APP_API_KEY')
app_api_secret = os.environ.get('APP_API_SECRET')
app_redirect_url = os.environ.get('APP_REDIRECT_URL')
app_auth_base_url = 'https://quickstart-c3b5f44b.myshopify.com/admin/oauth/authorize'
app_token_url = 'https://quickstart-c3b5f44b.myshopify.com/admin/oauth/access_token'

@app.route('/')
def index():
    return 'Hello, welcome to your app!'

@app.route('/install')
def install():
    shop = request.args.get('shop')  # Retrieve the actual shop name from the request
    auth_url = app_auth_base_url.format(shop=shop)
    auth_url += f'?client_id={app_api_key}&redirect_uri={app_redirect_url}&grant_options[]=per-user'
    return redirect(auth_url)

@app.route('/api/callback')
def oauth_callback():
    code = request.args.get('code')
    shop = request.args.get('shop')
    token_url = app_token_url.format(shop=shop)
    data = {
        'client_id': app_api_key,
        'client_secret': app_api_secret,
        'code': code
    }
    print(f'Authorization Code: {code}')
    response = requests.post(token_url, data=data)

    if response.ok:
        access_token = response.json().get('access_token')
        print(access_token)

        # Returning a simple response for demonstration purposes
        return f'Token obtained and authorized: {access_token}'
    else:
        return f'Error getting access token: {response.text}', 500  # Return an error response with status code

if __name__ == '__main__':
    app.run(debug=True)