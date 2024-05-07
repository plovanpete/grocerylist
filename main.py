from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from Backend.groceries.routes.groceries import grocery_router


app = FastAPI()

app.include_router(grocery_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this to allow requests from specific origins
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

@app.get("/")
async def view_index():
    return FileResponse("./FrontEnd/groceries/views/index.html")


# *NEW* Add this line of code to allow importing javascript files!
app.mount("/groceries", StaticFiles(directory="FrontEnd/groceries"), name="groceries")
