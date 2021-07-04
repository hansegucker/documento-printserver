#!/bin/bash
poetry export --without-hashes > requirements.txt
sed -i '/^pillow.*$/d' requirements.txt
dpkg-buildpackage -us -uc -b
