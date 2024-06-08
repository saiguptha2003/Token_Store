
#install the virtualenv
```bash
python -m venv fastapi-env
```

#start the virtualenv

```bash
./fastapi-env/Scripts/activate.bat
```

#install all the dependencies
```bash
pip install -r requirements.txt
```

#start the app
```bash
python -m uvicorn main:app --reload
```