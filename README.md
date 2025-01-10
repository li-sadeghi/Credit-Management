# Tabdeal-Project
This is a mini project to enter the Tabdeal company.

---

## How to Run

### Using Docker

1. Build and start the containers:
```
docker compose up -d
```

2. Apply database migrations:
```
dcoker compose exec app bash python manage.py migrate
```


## Using Python:
1. Create a virtual environment:
```
python -m venv .venv
```

2. Activate the virtual environment:
```
source .venv/bin/activate
```

3. Install the dependencies:
```
pip install -r requirements.in
```

4. Apply database migrations:
```
python manage.py migrate
```
