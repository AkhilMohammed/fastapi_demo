from typing import Pattern
import uvicorn

from fastapi import Depends, FastAPI, HTTPException
import os
# from fastapi_sqlalchemy import DBSessionMiddleware
# from fastapi_sqlalchemy import db
import models
# from models import User as baseuser, Mobile,Channel,Group,Message
import schema
from dotenv import load_dotenv
from sqlalchemy.orm import Session, session
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, ".env"))
from database import SessionLocal, engine
import uuid
from sqlalchemy import or_
from datetime import datetime
import re
models.Base.metadata.create_all(bind=engine)

app = FastAPI()
# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



@app.post("/mobile/", response_model=schema.Mobile)
def create_mobile(mobile: schema.Mobile, db: Session = Depends(get_db)):
    '''
        API Name: create_mobile
        purpose : To add a valid 10 digit number that starts wih 7or 8 or 9
        permission : permission not required
        parameters :
                    number = string (of 10 digits)
        request body :
                    "number" : "9989988988"
        response body :
                    {
                        "number" : "9989988988"
                    } 
    '''
    number = re.fullmatch("[7-9]\d{9}",mobile.number)
    if not number:
        raise HTTPException(status_code=400, detail="please add valid number")
    db_mobile = models.Mobile(number=mobile.number)
    db.add(db_mobile)
    db.commit()
    db.refresh(db_mobile)
    return db_mobile


@app.post("/bulkmobile/")
def create_BulkMobile(db: Session= Depends(get_db)):
    '''
        API Name: create_BulkMobile
        Method : POST
        purpose : To create  9 numbers for easily adding
        permission : permission not required
        parameters :
                    None
        request body :
                    None
        response body :
                    {
                        "data": None,
                        "message": "Success"
                    } 
    '''
    mobileList = ['9123456784','8123456784','7123456785',
                    '9080390801','9080123456','9123456789',
                    '9080790807','9123456780','7878789089']
    try:
        for number in mobileList:
            db_mobile = models.Mobile(number= number)
            db.add(db_mobile)
        db.commit()
        return {"data":None,"message":"Success"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/getNumber/{current_number}")
def get_number(current_number: str ,db: Session= Depends(get_db)):
    '''
        API Name: get_number
        Method: GET
        purpose : To get all the numbers other than the given number
        permission : permission not required
        parameters :
                    current_number = string (of 10 digits)
        request body :
                    "current_number" : "9989988988"
        response body :
                    {
                    "data": [
                        "9123456784",
                        "8123456784",
                        "7123456785",
                        "9086012345",
                        "90860123456",
                        "908601234567"
                    ],
                    "message": "Success"
                    }
    '''
    try:
        mobileList = []
        mobiles = db.query(models.Mobile).filter(models.Mobile.number!= current_number).all()
        for mobile in mobiles:
            mobileList.append(mobile.number)
        return {"data":mobileList,"message":"Success"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/checkConnection/{current_number}/{other_number}")
def get_connection(current_number: str, other_number: str, db: Session = Depends(get_db)):
    try:
        groupName1 = current_number+"-"+other_number
        groupName2 = other_number+"-"+current_number
        try:
            checkGroup = db.query(models.Channel).filter
            (or_(models.Channel.channelName == groupName1,models.Channel.channelName == groupName2)).one()
            messageList = []
            messages = db.query(models.Message).join(models.Mobile, models.Message.mobile_id == models.Mobile.id).filter
            (models.Message.channel_id == checkGroup.id).order_by(models.Message.createdTime.desc()).all()
            for message in messages:
                data = {
                    "sender" : message.mobile.number,
                    "message": message.message,
                    "messageId": message.messageID,
                    "reciever": other_number if message.mobile.number == current_number else current_number,
                    "createdTime": datetime.timestamp(message.createdTime)
                }
                messageList.append(data)
            currentUser = db.query(models.Mobile).filter(models.Mobile.number == current_number).one() 
            finalData = {
                "messageList" : messageList,
                "mobile_id" : currentUser.id,
                "channel_id" : checkGroup.id
            }
            return {"data":finalData,"message":"Success"}
        except:
            ''''
            checkGroup = db.query(models.Channel).filter
            (or_(models.Channel.channelName == groupName1,models.Channel.channelName == groupName2)).count()
            if checkGroup:
                raise HTTPException(status_code=400, detail="Something went wrong")
            '''
            db_channel = models.Channel(channelName=groupName1)
            db.add(db_channel)
            db.commit()
            db.refresh(db_channel)
            try:
                numberList = [current_number, other_number]
                for i in numberList:
                    mobile = db.query(models.Mobile).filter(models.Mobile.number ==i).one()
                    db_group = models.Group(mobile_id=mobile.id,Channel_id=db_channel.id)
                    db.add(db_group)
                db.commit()
                currentUser = db.query(models.Mobile).filter(models.Mobile.number == current_number).one()
                finalData = {
                    "messageList" : [],
                    "mobile_id" : currentUser.id,
                    "channel_id" : db_channel.id
                }
                return {"data":[],"message":"Success"}
            except Exception as e:
                db.rollback()
                raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/createMessage/")
def create_message(message: schema.Message, db: Session= Depends(get_db)):
    '''
        API Name: create_message
        purpose : To write a message in particular channel
        Method : POST
        permission : permission not required
        parameters :
                    message = string
                    mobile_id = int
                    channel_id = int
        request body :
                    {
                        "message": "string",
                        "channel": 0,
                        "mobile": 0
                    }
        response body :
                    {
                        "data" : "Success"
                    } 
    '''
    try:
        db_message = models.Message(message= message.message, channel_id=message.channel,mobile_id = message.mobile)
        db.add(db_message)
        db.commit()
        return {"data":"success"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/getmessages/{channel_id}")
def get_messages(channel_id:int, db: Session= Depends(get_db)):
    try:
        messageList = []
        messages = db.query(models.Message).filter(models.Message.channel_id == channel_id).all()
        for message in messages:
            messageList.append(message)
        return {"data":messageList,"message":"success"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

