import subprocess  # noqa
import time

import requests
from barcode import Code128
from barcode.writer import ImageWriter
from escpos.printer import Usb

from .config import settings

# Read vendor and product IDs from config and setup printer
raw_vendor = settings.get("printer.vendor")
raw_product = settings.get("printer.product")
vendor = int(f"0x{raw_vendor}", 16)
product = int(f"0x{raw_product}", 16)
print(f"Printer: Vendor: {raw_vendor} ({vendor}); Product: {raw_product} ({product})")
printer = Usb(vendor, product)


def print_info(document, categories=None):
    """Print report info page."""
    if categories is None:
        categories = {}
    if document["category"]:
        current_category = categories[document["category"]]
        cat_list = [current_category]

        while current_category["parent"]:
            cat_list.insert(0, categories[current_category["parent"]])
            current_category = categories[current_category["parent"]]
    else:
        cat_list = []

    printer.set(font="a", align="center")
    printer.text("DOCUMENTO - Archivetikett\n")
    printer.set(font="a", double_height=True, align="right", underline=False)
    printer.text("NR. {}\n".format(document["id"]))

    printer.set(font="b", align="left")
    printer.text("Titel:\n")
    printer.set(font="a", double_height=True, align="left", underline=True)
    printer.textln(document["name"])

    printer.set(font="b", align="left")
    printer.text("Zeitpunkt der Archivierung:\n")
    printer.set(font="a", double_height=False, align="left", underline=False)
    printer.textln(document["added_at"])

    printer.set(font="b", align="left")
    printer.text("Kategorie:\n")
    printer.set(font="a", double_height=False, align="center", underline=False)
    cat_names = ["[" + cat["name"] + "]\n" for cat in cat_list]
    printer.text("V\n".join(cat_names))

    printer.set(font="b", align="left")
    printer.text("Barcode:\n")
    barcode = document["barcode"]

    writer = ImageWriter()
    code = Code128(barcode, writer=writer).render(
        {"module_width": 0.4, "module_height": 5.0, "text_distance": 3.0}
    )
    printer.image(code, center=True)

    printer.ln(3)
    printer.control("LF")


base_url = settings.get("server.url")
login_url = base_url + "/api/auth/login/"
jobs_url = base_url + "/api/print_jobs/"
categories_url = base_url + "/api/categories/"


def print_server():
    while True:
        # Get auth token
        r = requests.post(
            login_url,
            json={
                "username": settings.get("server.username"),
                "password": settings.get("server.password"),
            },
        )
        token = r.json()["token"]
        headers = {"Authorization": f"Token {token}"}

        # Fetch print jobs
        jobs = requests.get(jobs_url, headers=headers).json()

        # Fetch categories
        categories = requests.get(categories_url, headers=headers).json()
        categories = {category["id"]: category for category in categories}

        for job in jobs:
            job_id = job["id"]
            report = job["report"]
            document = job["document"]
            document_id = document["id"]
            document_name = document["name"]

            print(f"Job {job_id}: {report}; Document {document_id}: {document_name}")

            printed = False
            if report == "barcode_label":
                label_url = base_url + document["barcode_label"]

                # Download barcode label
                r = requests.get(label_url)
                with open("barcode-tmp.pdf", "wb") as f:
                    f.write(r.content)

                # Send barcode label to printer
                subprocess.Popen(  # noqa
                    ["lp", "-d", settings.get("barcode_printer.name"), "barcode-tmp.pdf"],
                    stderr=subprocess.DEVNULL,
                    stdout=subprocess.DEVNULL,
                )  # noqa
                printed = True

            elif report == "info_page":
                print_info(document, categories)
                printed = True

            # Mark print job as printed
            if printed:
                r3 = requests.post(f"{jobs_url}{job_id}/mark_as_printed/", headers=headers)

        time.sleep(3)


if __name__ == "__main__":
    print_server()
