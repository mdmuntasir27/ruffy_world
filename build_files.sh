#!/bin/bash
set -e
echo "==> Preparing static output directory..."
mkdir -p staticfiles/static

echo "==> Installing Python dependencies..."
python3 -m pip install -r requirements.txt || pip install -r requirements.txt

echo "==> Running database migrations..."
python3 manage.py migrate --noinput || python manage.py migrate --noinput

echo "==> Seeding initial application data..."
python3 manage.py populate_sample_pets || python manage.py populate_sample_pets
python3 manage.py populate_store || python manage.py populate_store
python3 manage.py populate_vets || python manage.py populate_vets

echo "==> Collecting static assets..."
python3 manage.py collectstatic --noinput --clear || python manage.py collectstatic --noinput --clear

# Ensure files exist both in staticfiles/ and staticfiles/static/ for seamless routing
cp -r staticfiles/* staticfiles/static/ 2>/dev/null || true

echo "==> Vercel build completed successfully!"
