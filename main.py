from fastapi import FastAPI, Depends, status
from fastapi.responses import JSONResponse
from schema import ServiceDeskCreate, ServiceDeskUpdate
from database.models import ServiceDesk
from database.database import get_db
from sqlalchemy.orm import Session
from database import models
from database.database import engine

app= FastAPI()
models.Base.metadata.create_all(engine)

@app.post("/service-desk/")
def create_service_desk(data: ServiceDeskCreate, db: Session = Depends(get_db)):
    """
    Create a new service desk ticket.

    Parameters:
    - data: ServiceDeskCreate - The data for creating the ticket.
    - db: Session - Database session dependency.

    Returns:
    - JSONResponse with success or error message.
    """
    try:
        new_ticket = ServiceDesk(
            title=data.title,
            description=data.description,
            priority=data.priority,
            status=data.status
        )
        db.add(new_ticket)
        db.commit()
        return JSONResponse(
                    status_code=status.HTTP_200_OK,
                    content={
                        'message': "Successfully created ticket"},
                )
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"message": "Failed to create ticket", "error": str(e)},
        )


@app.put("/service-desk/{ticket_id}")
def update_service_desk(ticket_id: int, data: ServiceDeskUpdate, db: Session = Depends(get_db)):
    """
    Update an existing service desk ticket.

    Parameters:
    - ticket_id: int - ID of the ticket to update.
    - data: ServiceDeskUpdate - The updated ticket data.
    - db: Session - Database session dependency.

    Returns:
    - JSONResponse with success or error message.
    """
    try:
        ticket = db.query(ServiceDesk).filter(ServiceDesk.id == ticket_id).first()
        if not ticket:
            return JSONResponse(
                        status_code=status.HTTP_404_NOT_FOUND,
                        content={
                            'message': "Ticket not found"},
                    )

        if data.title:
            ticket.title = data.title
        if data.description:
            ticket.description = data.description
        if data.priority:
            ticket.priority = data.priority
        if data.status:
            ticket.status = data.status

        db.commit()
    
        result={
            "id": ticket.id,
            "title": ticket.title,
            "description": ticket.description,
            "priority": ticket.priority,
            "status": ticket.status
        }
        return JSONResponse(
                    status_code=status.HTTP_200_OK,
                    content={
                        "Message": "Successfully updated tickect details",
                        'Result': result},
                )
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"message": "Failed to update ticket", "error": str(e)},
        )


@app.get("/service-desk/{ticket_id}")
def get_service_desk(ticket_id: int, db: Session = Depends(get_db)):
    """
    Retrieve details of a specific service desk ticket.

    Parameters:
    - ticket_id: int - ID of the ticket to retrieve.
    - db: Session - Database session dependency.

    Returns:
    - JSONResponse with ticket details or error message.
    """
    try:
        ticket = db.query(ServiceDesk).filter(ServiceDesk.id == ticket_id).first()
        if not ticket:
            return JSONResponse(
                    status_code=status.HTTP_404_NOT_FOUND,
                    content={
                        'message': "Ticket not found"},
                )
        result={
            "id": ticket.id,
            "title": ticket.title,
            "description": ticket.description,
            "priority": ticket.priority,
            "status": ticket.status
        }
        return JSONResponse(
                    status_code=status.HTTP_200_OK,
                    content={
                        'Result': result},
                )
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"message": "Failed to fetch ticket", "error": str(e)},
        )


@app.get("/service-desk/")
def get_all_service_desks(db: Session = Depends(get_db)):
    """
    Retrieve details of all service desk tickets.

    Parameters:
    - db: Session - Database session dependency.

    Returns:
    - JSONResponse with a list of all tickets or error message.
    """
    try:
        tickets = db.query(ServiceDesk).all()
        result=[
            {
                "id": ticket.id,
                "title": ticket.title,
                "description": ticket.description,
                "priority": ticket.priority,
                "status": ticket.status
            }
            for ticket in tickets
        ]

        return JSONResponse(
                    status_code=status.HTTP_200_OK,
                    content={
                        "Message": "Successfully fetched all tickect details",
                        'Result': result},
                )
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"message": "Failed to fetch tickets", "error": str(e)},
        )


