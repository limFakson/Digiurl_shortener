# Exit on error
set -o errexit

# Modify this line as needed for your package manager (pip, poetry, etc.)
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt

#Appliy database migrations
python3 manage.py makemigrations --no-input
python3 manage.py migrate --no-input

# Convert static asset files
python3 manage.py collectstatic --no-input


#start tailwind