import asyncio
from typing import Any, Mapping
from flask import Response, request
from flask import Flask, redirect
import requests
from urllib.parse import urlsplit, parse_qs
from creds import CLIENT_ID, CLIENT_SECRET, REDIRECT_URL, SCOPES_LIST

# define the Flask APP
app: Flask = Flask(__name__)
# debug mode is enabled to show the backend operations
debug: bool = True


# ---------------------------------- #
class Utils:
    """
    Just a collection of usefull methods to work with incomming request
    """
    
    @staticmethod
    def parse_incomming_query(request_url: str) -> Mapping[str, Any]:
        parsed_query = urlsplit(request_url).query
        return parse_qs(parsed_query)
    
    @staticmethod
    def get_shop_name_from_query(parsed_query_params: Mapping[str, Any]) -> str:
        return parsed_query_params.get("shop")[0]
    
    @staticmethod
    def get_auth_code_from_query(parsed_query_params: Mapping[str, Any]) -> str:
        return parsed_query_params.get("code")[0]


class ProcessInstallRequest:
    """
    Accepts, pocesses, pushes the USER to the Grant Screen
    """
    
    def __init__(self, debug: bool):
        self.debug = debug
        
    async def run(self):
        return await self.install()
        
    async def verify_request(self, request_url: str) -> bool:
        """
        ! FOR THIS DEMO THE VERIFICATION OF THE RERQUST IS OMMITED !
        
        However, for `PRODUCTION` usage, this should be done worspace/source/ based.
        
        Request verification guide:
        https://shopify.dev/docs/apps/auth/oauth/getting-started#step-2-verify-the-installation-request
        """
        # default verification status
        is_verified = False
    
        if request_url:
            # SHA-256 hash verification code here....
            
            # 1) parse the query
            # 2) save and remove `hmac` param from the request
            # 3) build the hash  using the rest of the query params and compare this hash to the `hmac` param, they should be equal
            
            # set the verificaion to `True` if `hmac` from request.url == hash computed from step 3.
            is_verified = True
        
        return is_verified    
        
    async def install(self):
        """
        Accepts and process the incomming app install request
        https://shopify.dev/docs/apps/auth/oauth/getting-started#step-3-ask-for-permission
        """
        
        await asyncio.sleep(1)
        
        # for debug
        if self.debug:
            print(f"INSTALL RECEIVED:\n {request.url}\n")
            print(f"DATA RECEIVED:\n {request.data}\n")
        
        if await self.verify_request(request.url):
        
            # parse incomming query
            incoming_params = Utils.parse_incomming_query(request.url)
            # get `shop name` from incomming request
            shop = Utils.get_shop_name_from_query(incoming_params)
            # comma separated scopes
            scopes = ",".join(SCOPES_LIST)
            # the `state`param `nonce` is a specific state param shopify asks for, if no state is provided
            state = "nonce"
            
            # form the redirect_url to GRANT SCREEN with CONSENT
            redirect_url = f"https://{shop}/admin/oauth/authorize?client_id={CLIENT_ID}&scope={scopes}&redirect_uri={REDIRECT_URL}&state={state}"
            
            # finally redirect user to the GRANT SCREEN
            return redirect(redirect_url, 301)
        else:
            return Response(f"The Installation request {request.url} could not be veified, or broken.", 400)


class CompleteOAuthFlow:
    """
    Completes the OAuth Flow using input pararms:
    :client_id
    :client_secret
    :shop_name
    :auth_code
    
    returns JSON with `access_token`
    """
    
    def __init__(self, debug: bool):
        self.debug = debug
        
    async def run(self):
        return await self.oauth_flow()
    
    async def get_access_token(self, auth_code: str, shop: str) -> Mapping[str, Any]:
        """
        Exchanges the `auth_code` to permanent `access_token`
        https://shopify.dev/docs/apps/auth/oauth/getting-started#step-5-get-an-access-token
        """
        method = "POST"
        access_token_url = f"https://{shop}/admin/oauth/access_token"
        params = {
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "code": auth_code,
        }
        response = requests.request(method=method, url=access_token_url, params=params)
        return response.json()
    
    async def oauth_flow(self):
        # sleep 1 sec
        await asyncio.sleep(1)
        # for debug
        if self.debug:
            print(f"DATA RECEIVED:\n {request.data}\n")
        
        # parse incomming query
        incoming_params = Utils.parse_incomming_query(request.url)
        # get the `auth_code` from incomming request query params
        auth_code = Utils.get_auth_code_from_query(incoming_params)
         # get `shop name` from incomming request
        shop = Utils.get_shop_name_from_query(incoming_params)
        # exchange the `auth_code` for `access_token`
        access_token = await self.get_access_token(auth_code, shop)
        
        return Response(f"Successfully Installed. The `access_token`: {access_token}", 200)


@app.route('/install', methods=["GET"])
async def install():
    return await ProcessInstallRequest(debug).run()

@app.route('/oauth_flow', methods=['POST', "GET"])
async def oauth_flow():
    return await CompleteOAuthFlow(debug).run()

if __name__ == '__main__':
    app.run(debug=debug, port=3000)
