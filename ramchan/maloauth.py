import requests
import json
import secrets

class oauth:
	def get_token(oauth_code, code_chan):
		data={
	    "client_id":"8b4ce93eea2158c15fd45812ee8f01c5",
	    "code":oauth_code,
	    "code_verifier":code_chan,
	    "grant_type":"authorization_code"
		}
		resp=requests.post(url='https://myanimelist.net/v1/oauth2/token', data=data)
		print(resp.text)
		data=json.loads(resp.text)
		return data['access_token'], data['refresh_token']

	def use_refresh_token(refresh_token):
		data={
	    "client_id":"8b4ce93eea2158c15fd45812ee8f01c5",
	    "refresh_token":refresh_token,
	    "grant_type":"refresh_token"
		}
		resp=requests.post(url='https://myanimelist.net/v1/oauth2/token', data=data)
		print(resp.text)
		data=json.loads(resp.text)
		return data['access_token'], data['refresh_token']

	def get_new_code_verifier() -> str:
		token = secrets.token_urlsafe(100)
		return token[:128]
		code_verifier = code_challenge = get_new_code_verifier()
		print(len(code_verifier))
		print(code_verifier)