from argparse import ArgumentParser

from stockxsdk import Stockx
import xlwt


# not sure about this, i think it's the right activity code
ACTIVITY_TYPE_SOLD = "480"

def write_size_report(file_name, sales):
    book = xlwt.Workbook()
    sizes = sorted({sale["shoeSize"] for sale in sales}, key=lambda x:float(x))
    for size in sizes:
        sheet = book.add_sheet(f"Size {size}")
        sheet.write(0, 0, "DATE")
        sheet.write(0, 3, "AMOUNT")

        size_sales = sorted(
            [sale for sale in sales if sale["shoeSize"] == size],
            key=lambda x: x["createdAt"])

        for i in range(0, len(size_sales)):
            date = size_sales[i]["createdAt"]
            sheet.write(i + 1, 0, date)
            sheet.write(i + 1, 3, f"${size_sales[i]['amount']}")
    book.save(file_name)
    return file_name

if __name__ == "__main__":

    # todo parse from args
    parser = ArgumentParser(
        description="Take a style number and generate a spreadsheet of sales from Stock X.")
    parser.add_argument("style_id", help="The style id for the shoe.")
    parser.add_argument("--size", help="Optionally restrict output to a single size.")
    parser.add_argument("--email", help="Email Address for your StockX account.")
    parser.add_argument("--password", help="Password for your StockX account.")
    parser.add_argument("--file", help="Name and location of file. Defaults to style_id.xls.")
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
    print("Writing spreadshet...")
    file_name = args.file or f"{args.style_id}.xls"
    write_size_report(file_name, sales)
    print(f"{file_name} saved.")
    exit(0)
