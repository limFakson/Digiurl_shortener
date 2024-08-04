# Install dependencies
pip install -r requirements.txt

# Collect static files
python manage.py collectstatic --noinput

#tailwind start build
python manage.py tailwind start