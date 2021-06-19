# documento-printserver
A print server for the documento document management system

## Features
- Prints info papers on any ESCPOS-compatible printer (optimised for 58mm)
- Prints barcodes label on special barcode printers using CUPS (downloads PDF from server)


## Setup udev

- `sudo cp 99-escpos.rules /etc/udev/rules.d/99-escpos.rules`
- Add user to group `dialout`
- Restart udev `sudo service udev restart` (In some new systems it is done with `sudo udevadm control --reload`)


