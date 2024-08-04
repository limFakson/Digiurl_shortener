# Exit on error
set -o errexit

# Modify this line as needed for your package manager (pip, poetry, etc.)
python3.9 pip install -r requirements.txt

# Convert static asset files
python3.9 manage.py collectstatic --no-input

# Apply any outstanding database migrations
python3.9 manage.py migrate

#start tailwind