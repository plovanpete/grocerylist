# grocerylist
A website keeping track of your grocery list!

![website](https://github.com/plovanpete/grocerylist/assets/145849883/f88ba444-d073-41e4-a77e-21bc7a1495c9)

## Instructions to start it and load it:
First, you'll want to create a virtual environment. Do so by using this command:
```
python -m venv venv
```
Do this command after you created your venv *(Only for Windows)*:
```
./venv/Scripts/activate  
```

Afterwards, install the requirements needed: 
```
pip install -r requirements.txt
```

You'll then have to connect to MongoDB. Start up MongoDB Compass and connect to the server!
Note that the db.py needs a url link to connect to the server.

Then, start up the actual backend server with this:
```
uvicorn main:app --reload
```
