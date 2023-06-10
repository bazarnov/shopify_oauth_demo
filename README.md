# Sign up, install and register NGROK

1. Download the `NGROK` from the webpage url https://ngrok.com/ and put it to the root folder next to `main.py` file.
2. Login to your account to see the installation details: https://dashboard.ngrok.com/get-started/setup
3. Provide the Auth for the `NGROK` service: 
```bash
# navigate to the ngok file folder saved after the download
cd <dir with ngrok>;

# It should echo the message that `auth token is saved in *.yaml` which is ok.
./ngrok config add-authtoken <YOUR TOKEN>

# run the service
./ngrok http 3000

# copy the value of `FROWARDING` from running `NGROK` instance, which should similar to this:
`https://c6b3-46-96-141-162.ngrok-free.app` (example)

```

### Edit your `CLIENT_ID`, `CLIENT_SECRET` for your `OAUTH SHOPIFY APP` in the `creds.py`:
```python
...
CLIENT_ID = ...
CLIENT_SECRET = ...
```

### Edit the `REDIRECT_URL` in the `creds.py` file
```python
...
REDIRECT_URL: str = "<ngrok_external_url>/oauth_flow"
```
where `<ngrok_external_url>` is the `Fowarding` value you may see after running the `NGROK`

## Run the `Flask` local instance from the root folder
```
python3 main.py
```

## Prepare two main `redirect_urls` to use within the `Shopify OAuth App (Setup)`

The `https://c6b3-46-96-141-162.ngrok-free.app` is the example external proxy instance, replace it with the real one obtained in `# Sign up, install and register NGROK`

1. Install request redirect_url, example: `https://c6b3-46-96-141-162.ngrok-free.app/install` as `APP URL`
2. Main redirect_url to exchange `code` for an `access_token`: `https://c6b3-46-96-141-162.ngrok-free.app/oauth_flow` as `Optional Redirect URL`
3. Save the changes

### Proceed with `Test Store` > select the store you want to authenticate > Press `Install Unlisted App`
Once done, you will be redirected to the `Optional redirect url` added to the `Shopify OAuth App (Setup)` ealier and will see the `access_token` on the page.
