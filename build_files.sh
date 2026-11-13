#!/bin/bash

echo "==> Vercel Static Build started..."

# Prepare static output folders
mkdir -p staticfiles/static

# Upgrade pip and install Python requirements
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt

# Collect static assets
python3 manage.py collectstatic --noinput --clear

# Ensure files exist both in staticfiles/ and staticfiles/static/ for flexible routing
cp -r staticfiles/* staticfiles/static/ 2>/dev/null || true

echo "==> Vercel Static Build completed successfully!"
