from typing import List, Optional
from uuid import UUID, uuid4
from datetime import datetime
from pydantic import BaseModel, EmailStr, Field


class Address(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    type: str
    street1: str
    street2: Optional[str] = None
    city: str
    state: str
    postalCode: str
    country: str


class Phone(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    type: str
    countryCode: str
    number: str
    extension: Optional[str] = None


class NotificationPreferences(BaseModel):
    email: bool
    sms: bool
    push: bool
    mail: bool


class Customer(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    firstName: str
    middleName: Optional[str]
    lastName: str
    email: EmailStr
    addresses: List[Address]
    phoneNumbers: List[Phone]
    notificationPreferences: NotificationPreferences
    createdAt: datetime = Field(default_factory=datetime.utcnow)
    updatedAt: datetime = Field(default_factory=datetime.utcnow)
