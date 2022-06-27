from typing import List
from fastapi import APIRouter, Depends, status
from app.data import database
from app.security import oauth2
from app.schemas import schemas, schemasReport
from sqlalchemy.orm import Session
from app.restApi.repository import blog

router = APIRouter(
    prefix="/blogs",
    tags=['Blogs']
)

dataBase = database.getDataBase


@router.get('/', response_model=List[schemasReport.ShowBlog])
def all(db: Session = Depends(dataBase), current_user: schemas.User = Depends(oauth2.getCurrentUser)):
    return blog.get_all(db)


@router.post('/', status_code=status.HTTP_201_CREATED)
def create(request: schemasReport.Blog, db: Session = Depends(dataBase), current_user: schemas.User = Depends(
    oauth2.getCurrentUser)):
    return blog.create(request, db)


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def destroy(id: int, db: Session = Depends(dataBase), current_user: schemas.User = Depends(oauth2.getCurrentUser)):
    return blog.destroy(id, db)


@router.put('/{id}', status_code=status.HTTP_202_ACCEPTED)
def update(id: int, request: schemasReport.Blog, db: Session = Depends(dataBase), current_user: schemas.User = Depends(
    oauth2.getCurrentUser)):
    return blog.update(id, request, db)


@router.get('/{id}', status_code=200, response_model=schemasReport.ShowBlog)
def show(id: int, db: Session = Depends(dataBase), current_user: schemas.User = Depends(oauth2.getCurrentUser)):
    return blog.show(id, db)