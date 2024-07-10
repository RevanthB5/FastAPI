from fastapi import FastAPI, Path, Query, HTTPException, status
import uvicorn

from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name:str
    price:float
    brand:str = None

# for updating we do not need to pass all the values 
# thats why we make all of them optional
class UpdateItem(BaseModel):
    name:str = None
    price: int = None
    brand:str = None

# inventory={
#     1:{
#         "name": "milk",
#         "price": 100,
#         "brand":"regular"
#     }
# }

inventory={}


# 1
@app.get("/")
def home():
    return {"Data":"Test"}

# 2
## path Parameters
## can add multiple path parameters
@app.get("/get_item/{item_id}/{name}")
def get_item(item_id: int,name: str):
    return inventory[item_id]

# 3
## Path(default_value,description): adds more DESCRIPTION and CONSTRAINTS 
#to the path parameters
@app.get("/get-item-path-function/{item_id}")
def get_item_path_function(item_id: int = Path(...,description="the ID of the item ud like to view",ge=1,le=1)):
    return inventory[item_id]


# # 4 
# ## Query parameters
# #http://127.0.0.1:8000/get-by-name?name=milk
# # " =None " makes the query parameter optional 

# @app.get("/get-by-name")
# def get_by_name(name:str=None):
#     for item_id in inventory:
#         if inventory[item_id]["name"] == name:
#             return inventory[item_id]
#     return {"Asked Data":"Not Found"}


# # 5
# ## multiple Query parameters we use "&"
# # ( "*" deals with the default arguements first error )
# @app.get("/get-by-name-multiple-query-params")
# def get_by_name_multiple_quert_params(*,name:str=None,type:int):
#     for item_id in inventory:
#         if inventory[item_id]["name"] == name:
#             return inventory[item_id]
#     return {"Asked Data":"Not Found"}


# # 6
# ## path parameter and query parameter together
# # http://127.0.0.1:8000/get-by-name-path-and-query-parameters/1?name=milk&type=1
# @app.get("/get-by-name-path-and-query-parameters/{item_id}")
# def get_by_name_path_and_query_parameters(*, item_id:int, name:str = Query(None, description="Enter the Name of the item"), type:int):
#     if inventory[item_id]["name"] == name:
#         return inventory[item_id]
#     return {"Asked Data":"Not Found"}


#--------------------------------------------------------------------------------------

# creating a new item in the inventory dictionary using POST
@app.post("/create-item/{item_id}")
def create_item(item_id:int, item:Item):
    if item_id in inventory:
        return {"Error": "Item already exists"}
    
    # inventory[item_id] = {"name":item.name, "brand":item.brand, "price":item.price}
    inventory[item_id] = item   #SHORTER FORM
    return inventory[item_id]


## Since we inserted and Item object into the inventory dictionary, we need to change 
#  the GET functions and the initial Inventory keys' values to item objects

# inventory[item_id]["name"] == newName      --X
# inventory[item_id].name == newName         --_/


# 6
## path parameter and query parameter together
# http://127.0.0.1:8000/get-by-name-path-and-query-parameters/1?name=milk&type=1
@app.get("/get-by-name-path-and-query-parameters/{item_id}")
def get_by_name_path_and_query_parameters(*, item_id:int, name:str = Query(None, description="Enter the Name of the item"), type:int):
    if inventory[item_id].name == name:
        return inventory[item_id]
    return {"Asked Data":"Not Found"}



#----------------------------------------------------------------------------------------------------
# updating existing items

@app.put("/update-item/{item_id}")
def update_item(item_id:int, item:UpdateItem):
    if item_id not in inventory:
        return {"Error":"item doesnt exist"}
    
    # inventory[item_id] = item
    #       OR
    
    if item.name != None: 
        inventory[item_id].name = item.name
    if item.price != None:
        inventory[item_id].price = item.price
    if item.brand!= None:
        inventory[item_id].brand = item.brand
    return inventory[item_id]


#----------------------------------------------------------------------------------------------------

# deleting items

# "..." means it is requeired
@app.delete("/delete-item")
def delete_item(item_id: int = Query(...,description="The id of the item to delete:",gt=0)):
    if item_id not in inventory:
        # return {"Error":"item doesnt exist"}
        raise HTTPException(status_code=404, detail="Item doesnt exist")
    del inventory[item_id]
    return {"Data":"Item Deleted"}
