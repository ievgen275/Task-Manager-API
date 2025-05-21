import uvicorn
from fastapi import FastAPI
from sqlalchemy import select
from dependencies import SessionDep
from database import engine
from routers.auth import router
from models.models import UserModel, TaskModel, Base
from sсhemas.schemas import UserSchema, TaskSchema
from routers.auth import pwd_context

app = FastAPI()
app.include_router(router)

# Point for create database table
@app.post("/setup-database", summary = "Create table database", tags = ["Database"])
async def setup_database():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    return {"message": "Table is create"}

# CRUD-point for users
@app.get("/users", summary = "Get all users", tags = ["General points for user"])
async def get_users(session: SessionDep):
    query = select(UserModel)
    result = await session.execute(query)
    return result.scalars().all()

@app.post("/add-user", summary = "Add user", tags = ["General points for user"])
async def add_user(client: UserSchema, session: SessionDep):
    new_client = UserModel (
        name = client.name,
        email = client.email,
        username = client.username,
        password = pwd_context.hash(client.password)
    )
    session.add(new_client)
    await session.commit()
    return {"message": "client add database"}

@app.put("/update-user/{client_id}", summary="Update user", tags = ["General points for user"])
async def update_user(user_id: int, user: UserSchema, session: SessionDep):
    result = await session.execute(
        select(UserModel).where(UserModel.id == user_id)
    )
    update_user = result.scalar_one_or_none()
    if update_user is None:
        return {"message": f"User with id {user_id} not found"}

    update_user.name = user.name
    update_user.email = user.email
    update_user.username = user.username

    await session.commit()
    return {"message": "List user is update"}

@app.delete("/delete-user/{client_id}", summary="Delete user", tags = ["General points for user"])
async def delete_user(user_id: int, session: SessionDep):
    result = await session.execute(
        select(UserModel).where(UserModel.id == user_id)
    )
    delete_client = result.scalar_one_or_none()
    if update_user is None:
        return {"message": f"User with id {user_id} not found"}

    await session.delete(delete_client)
    await session.commit()

    return {"message": "User is delete"}

# CRUD-point for task
@app.get("/tasks", summary="Get all task for user", tags=["General points for task"])
async def get_tasks(session: SessionDep):
    query = select(TaskModel)
    result = await session.execute(query)
    return result.scalars().all()

@app.post("/add-task", summary="Add task", tags=["General points for task"])
async def add_task(task: TaskSchema, session: SessionDep):
    new_task = TaskModel(
        title = task.title,
        details = task.details,
        user_id = task.user_id
    )
    session.add(new_task)
    await session.commit()
    return {"message": "task is add database"}


@app.put("/update-task/{task_id}", summary="Update task", tags=["General points for task"])
async def update_task(task_id: int, task: TaskSchema, session: SessionDep):
    result = await session.execute(
        select(TaskModel).where(TaskModel.id == task_id)
    )
    update_task = result.scalar_one_or_none()
    if update_task is None:
        return {"message": f"User with id {task_id} not found"}

    update_task.title = task.title
    update_task.details = task.details

    await session.commit()
    return {"message": "List task is update"}


@app.delete("/delete-task/{task_id}", summary="Delete task", tags=["General points for task"])
async def delete_task(task_id: int, session: SessionDep):
    result = await session.execute(
        select(TaskModel).where(TaskModel.id == task_id)
    )
    delete_task = result.scalar_one_or_none()
    if delete_task is None:
        return {"message": f"User with id {task_id} not found"}

    await session.delete(delete_task)
    await session.commit()

    return {"message": "Task is delete"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0")