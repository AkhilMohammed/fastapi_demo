from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import backref, relationship
from datetime import datetime
from sqlalchemy.sql.expression import update
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.dialects.postgresql import UUID
import uuid
from sqlalchemy.sql.sqltypes import DateTime

Base = declarative_base()


class User(Base):
    __tablename__ = "users"    
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String,)
    last_name = Column(String)
    age = Column(Integer)
    

class Mobile(Base):
    __tablename__ = "mobiles"
    id = Column(Integer,primary_key=True, index=True)
    number = Column(String, unique=True)
    createdTime = Column(DateTime,default=datetime.now())
    updatedTime = Column(DateTime, default=datetime.now())
    channels = relationship("Channel", secondary="groups")


class Channel(Base):
    __tablename__ = "channels"
    id = Column(Integer,primary_key=True, index=True)
    channelName = Column(String,unique=True)
    createdTime = Column(DateTime, default=datetime.now())
    updatedTime = Column(DateTime, default=datetime.now())
    mobiles = relationship("Mobile", secondary="groups")


class Group(Base):
    __tablename__ = "groups"
    id = Column(Integer, primary_key=True)
    mobile_id = Column(Integer, ForeignKey('mobiles.id'))
    Channel_id = Column(Integer, ForeignKey('channels.id'))
    createdTime = Column(DateTime, default=datetime.now())
    mobile = relationship(Mobile, backref=backref("groups", cascade="all, delete-orphan"))
    channel = relationship(Channel, backref=backref("groups", cascade="all, delete-orphan"))


class Message(Base):
    __tablename__ = "messages"
    messageID = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    message = Column(String)
    createdTime = Column(DateTime, default=datetime.now())
    updatedTime = Column(DateTime, default=datetime.now())
    channel_id = Column(Integer, ForeignKey("channels.id"))
    mobile_id = Column(Integer, ForeignKey("mobiles.id"))
    channel = relationship(Channel, backref=backref("channels", cascade="all, delete-orphan"))
    mobile = relationship(Mobile, backref=backref("mobiles", cascade="all, delete-orphan"))
# Channel.messages = relationship("Message", order_by=Message.messageID, back_populates= "channels")

