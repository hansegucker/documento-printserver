# documento-printserver
A print server for the documento document management system

## Features
- Prints info papers on any ESCPOS-compatible printer (optimised for 58mm)
- Prints barcodes label on special barcode printers using CUPS (downloads PDF from server)


## Setup udev

- `sudo cp 99-escpos.rules /etc/udev/rules.d/99-escpos.rules`
- Add user to group `dialout`
- Restart udev `sudo service udev restart` (In some new systems it is done with `sudo udevadm control --reload`)


## Copyright

Copyright © 2020, 2021 Jonathan Weth <dev@jonathanweth.de>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
