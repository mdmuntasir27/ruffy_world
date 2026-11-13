#!/bin/bash
echo "==> Building Ruffy World for Vercel Serverless Deployment..."
python3 -m pip install -r requirements.txt
python3 manage.py migrate --noinput
python3 manage.py populate_sample_pets
python3 manage.py populate_store
python3 manage.py populate_vets
python3 manage.py collectstatic --noinput --clear
echo "==> Vercel build completed successfully!"
