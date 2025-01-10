# Credit-Management
This is a mini project for managing credit between sellers.

---

## How to Run

Set the environment. for example:
```
export ENV=development
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

### Using Docker

1. Build and start the containers:
```
docker compose up -d
```

2. Apply database migrations:
```
dcoker compose exec app bash python manage.py migrate
```


