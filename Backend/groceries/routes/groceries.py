from fastapi import APIRouter, HTTPException, status, Depends, Path
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorCollection
from ..model.GroceriesModel import GroceryRequest
from databases.db import get_mongo_client
from bson import ObjectId

# Optional, if you want to see logs of all your things
import logging

grocery_router = APIRouter()

async def get_grocery_collection(client: AsyncIOMotorClient) -> AsyncIOMotorCollection:
    return client["grocerylist"]["groceries"]

# Configures logging
logging.basicConfig(filename='app.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


# Function to create a grocery item
@grocery_router.post("/groceries/", status_code=status.HTTP_201_CREATED, response_model=GroceryRequest)
async def create_grocery(grocery: GroceryRequest, client: AsyncIOMotorClient = Depends(get_mongo_client)) -> GroceryRequest:
    grocery_collection = await get_grocery_collection(client)
    result = await grocery_collection.insert_one(grocery.dict())  # Convert GroceryRequest to dictionary
    inserted_grocery = await grocery_collection.find_one({"_id": result.inserted_id})

    if inserted_grocery is None:
        raise HTTPException(status_code=404, detail="Grocery not found")

    # Extract the desired fields from the inserted_grocery document
    formatted_item = {
        "id": str(inserted_grocery["_id"]),  # Convert ObjectId to string
        "title": inserted_grocery["title"],
        "quantity": inserted_grocery["quantity"]
    }

    # Logging
    logging.info(f'Grocery Created: {formatted_item["title"]} with {formatted_item["quantity"]}. '
                 f'The id for the grocery is {formatted_item["id"]}')

    return formatted_item


# Function to get a grocery by id
@grocery_router.get("/groceries/{grocery_id}")
async def get_grocery_by_id(
    grocery_id: str, client: AsyncIOMotorClient = Depends(get_mongo_client)
) -> dict:
    groceries_collection = await get_grocery_collection(client)
    grocery = await groceries_collection.find_one({"_id": ObjectId(grocery_id)})
    if grocery:
        # Convert ObjectId to string for JSON serialization
        grocery["_id"] = str(grocery["_id"])
        
        # Logging
        logging.info(f'Grocery Retrieved: {grocery}')
        
        return grocery
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"The grocery with ID '{grocery_id}' is not found",
        )
    

# Function to get all groceries
@grocery_router.get("/allgroceries/")
async def get_groceries(client: AsyncIOMotorClient = Depends(get_mongo_client)):
    groceries_collection = await get_grocery_collection(client)
    groceries = await groceries_collection.find().to_list(1000)  # Adjust the limit as needed
    
    # Convert ObjectId to string for each document
    for grocery in groceries:
        grocery["_id"] = str(grocery["_id"])
    
    return groceries


# Function to update a grocery item
@grocery_router.put("/groceries/{grocery_id}")
async def update_grocery(
    grocery_id: str, updated_grocery: GroceryRequest, client: AsyncIOMotorClient = Depends(get_mongo_client)
) -> dict:
    updated_grocery_dict = updated_grocery.dict()

    groceries_collection = await get_grocery_collection(client)
    result = await groceries_collection.update_one(
        {"_id": ObjectId(grocery_id)},
        {"$set": updated_grocery_dict}
    )

    if result.modified_count > 0:
        logging.info(f'Grocery item with ID "{grocery_id}" was successfully updated!')
        return {"msg": f"Updated grocery item with ID {grocery_id} successfully!"}
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No grocery item found with ID '{grocery_id}'"
        )



# Function to delete a grocery item by name and address
@grocery_router.delete("/groceries/{grocery_id}")
async def delete_grocery(grocery_id: str, client: AsyncIOMotorClient = Depends(get_mongo_client)):
    groceries_collection = await get_grocery_collection(client)
    result = await groceries_collection.delete_one({"_id": ObjectId(grocery_id)})
    if result.deleted_count == 1:
        logging.info(f'Grocery item with ID "{grocery_id}" was successfully deleted!')
        return {"msg": f'Grocery item with ID "{grocery_id}" was successfully deleted!'}
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"The grocery item with ID '{grocery_id}' is not found"
        )


