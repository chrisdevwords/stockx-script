from argparse import ArgumentParser
import json

from stockxsdk import Stockx

# not sure about this...
ACTIVITY_TYPE_SOLD = "480"

if __name__ == "__main__":

    # todo parse from args
    parser = ArgumentParser(
        description="Take a style number and get the latest sales from Stock X.")
    parser.add_argument("style_id", help="The style id for the shoe.")
    parser.add_argument("--size", help="Optionally restrict output to a single size.")
    parser.add_argument("--email", help="Email Address for your StockX account.")
    parser.add_argument("--password", help="Password for your StockX account.")
    args = parser.parse_args()
    logged_in = False
    auth_headers = {}
    stx = Stockx()
    if args.email and args.password:
        logged_in = stx.authenticate(args.email, args.password)
        auth_header = stx.headers
    product_id = stx.get_first_product_id(args.style_id)
    # this is how you get the sales info for the chart...
    sales = stx._Stockx__get_activity(product_id, ACTIVITY_TYPE_SOLD)
    if args.size:
        sales = [s for s in sales if s["shoeSize"] == args.size]
    print("Most recent sale: ${localAmount} on {createdAt}".format(**sales[0]))
    sales = sorted(sales, key=lambda x: x["amount"])
    print("Highest sale: ${localAmount} on {createdAt}".format(**sales[-1]))
    print("Lowest sale: ${localAmount} on {createdAt}".format(**sales[0]))
    #print(json.dumps(sales, indent=True))
    exit(0)
