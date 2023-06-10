# CRREDENTIALS to complete OAUTH FLOW
# Client Id for OAuth Application
CLIENT_ID: str = "____"
# Client Secret for OAuth Application
CLIENT_SECRET: str = "____"
# The backend redirect url
REDIRECT_URL: str = "<ngrok_external_url>/oauth_flow"

# ---------------------------------- #
# declare the scopes needed for `source-shopify`
SCOPES_LIST: list[str] = [
    "read_themes",
    "read_orders",
    "read_all_orders",
    "read_assigned_fulfillment_orders",
    "read_content",
    "read_customers",
    "read_discounts",
    "read_draft_orders",
    "read_fulfillments",
    "read_locales",
    "read_locations",
    "read_price_rules",
    "read_products",
    "read_product_listings",
    "read_shopify_payments_payouts"
]
