from fastapi import FastAPI, Query, Depends
from typing import Optional, Union
from datetime import date
from pydantic import BaseModel, Field
from App.bookings.routers import router as router_bookings

import uvicorn


app = FastAPI()
app.include_router(router_bookings)

class HotelsSearchArgs:
    def __init__(
        self,
        location: str,
        date_from: date, 
        date_to: date,
        stars: Optional[int] = Query(None, ge=1, le=5),
        has_spa: Optional[bool] = None
    ):
        self.location = location
        self.date_from = date_from
        self.date_to = date_to
        self.stars = stars
        self.has_spa = has_spa


class SHotel(BaseModel):
    address: str
    name: str
    stars: int

    class Config:
        orm_mode = True

@app.get('/hotels/')
def get_hotels(search_args: HotelsSearchArgs = Depends()):
    return search_args

@app.get('/hotels/{hotel_id}/')
def get_hotels_id(
    hotel_id: int, 
    date_from: str, 
    date_to: str
):
    return hotel_id, date_from, date_to

class SBooking(BaseModel):
    room_id: int
    date_from: date
    date_to: date

@app.post('/bookings/')
def add_booking(booking: SBooking):
    pass

    

def main():
    config = uvicorn.run('main:app', host='127.0.0.1', port=8000, reload=True)
    server = uvicorn.Server(config)
    server.serve()

if __name__ == '__main__':
    main()