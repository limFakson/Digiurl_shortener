# Exit on error
set -o errexit

# Modify this line as needed for your package manager (pip, poetry, etc.)
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt

#Appliy database migrations
yes yes | python3 manage.py makemigrations
python3 manage.py migrate --no-input

# Convert static asset files
yes | python3 manage.py collectstatic


#start tailwind