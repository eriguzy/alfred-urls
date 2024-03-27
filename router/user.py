"""Routes related to User Account creation."""

from fastapi import APIRouter, Depends, Request, Form
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from storage import database, model
from utils.service import bcrpyt_context
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from utils.rate_limit import rate_limited


router = APIRouter(prefix="/user", tags=["user"])

templates = Jinja2Templates(directory="templates")


#register page route
@router.get("/sign-up", response_class=HTMLResponse)
@rate_limited(max_calls=3, time_frame=60)
async def signup(request: Request):
    return templates.TemplateResponse("sign-up.html", {"request": request})

#NEW USER REGISTRATION
@router.post('/sign-up', response_class=HTMLResponse)
async def signup(
    request: Request, 
    fullname: str = Form(...),
    email: str = Form(...),
    tel: str = Form(...), 
    username: str = Form(...), 
    password: str = Form(...), 
    password2: str = Form(...),
    db:Session=Depends(database.get_db)
    ):
    
    msg = []
    
    if password != password2:
        msg.append("Passwords mismatch")
        return templates.TemplateResponse("sign-up.html", {
            "request": request, 
            "msg": msg,
            'email': email,
            "fullname": fullname,  
            "tel": tel,
            "username": username,
        })

    new_user = model.USER(
        email = email,
        fullname = fullname,
        tel = tel,
        username = username,
        password = bcrpyt_context.hash(password),
    )
    
    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        msg.append("Registration successful")
        return templates.TemplateResponse(
            "sign-in.html", 
            {"request": request, 
                "msg": msg,
            })
    
    except IntegrityError:
        msg.append("Email already taken")
        return templates.TemplateResponse("sign-up.html", {
            "request": request, 
            "msg": msg,
            "email": email,
            "fullname": fullname,  
            "tel": tel,
            "username": username,
        })


# #EDITING USER INFORMATION BY User ONLY
# @router.put("/edit_user")
# async def edit_username(username, db:Session=Depends(database.get_db), token:str=Depends(oauth2_scheme)):
    
#     # authentication
#     user = get_user_from_token(db, token)
    
#     #Authorazation
#     scan_db = db.query(model.USER).filter(model.USER.email == user.email)
#     if not scan_db.first():
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED, 
#             detail="UNAUTHORIZED USER"
#         )
    
#     scan_db.update({model.USER.username:username})
#     db.commit()
#     raise HTTPException(
#             status_code=status.HTTP_202_ACCEPTED, 
#             detail='Information updated successfully'
#         )