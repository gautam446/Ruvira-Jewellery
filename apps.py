from fastapi import FastAPI, Request, Form, UploadFile, File
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
import shutil
import os
import cloudinary
import cloudinary.uploader

from database import engine, SessionLocal

from models.product import Product
from models.category import Category
from models.review import Review


app = FastAPI()

cloudinary.config(
    cloud_name="dkkvyyyio",
    api_key="261945847968321",
    api_secret="mI5YC23G-55tF6ITRhkEXQdv0i8"
)


Product.metadata.create_all(bind=engine)
Category.metadata.create_all(bind=engine)
Review.metadata.create_all(bind=engine)


app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static"
)

app.mount(
    "/uploads",
    StaticFiles(directory="uploads"),
    name="uploads"
)


templates = Jinja2Templates(
    directory="templates"
)


os.makedirs(
    "uploads",
    exist_ok=True
)

os.makedirs(
    "uploads/videos",
    exist_ok=True
)
@app.post("/add-product")
async def save_product(
    name: str = Form(...),
    price: int = Form(...),
    description: str = Form(...),
    category: str = Form(...),
    image_size: str = Form(...),
    image: UploadFile = File(...),
    video: UploadFile = File(None)
):

    upload_result = cloudinary.uploader.upload(image.file)
    image_url = upload_result["secure_url"]

    video_name = ""

    if video and video.filename != "":

        video_path = f"uploads/videos/{video.filename}"

        with open(video_path, "wb") as buffer:
            shutil.copyfileobj(
                video.file,
                buffer
            )

        video_name = video.filename

    db = SessionLocal()

    product = Product(
        name=name,
        price=price,
        description=description,
        image=image_url,
        image_size=image_size,
        category=category,
        video=video_name
    )

    db.add(product)
    db.commit()
    db.close()

    return RedirectResponse(
        url="/products",
        status_code=303
    )
@app.post("/edit/{product_id}")
async def update_product(
    product_id: int,
    name: str = Form(...),
    price: int = Form(...),
    description: str = Form(...),
    category: str = Form(...),
    image_size: str = Form(...),
    image: UploadFile = File(None),
    video: UploadFile = File(None)
):

    db = SessionLocal()

    product = db.query(Product).filter(
        Product.id == product_id
    ).first()

    if product:

        product.name = name
        product.price = price
        product.description = description
        product.category = category
        product.image_size = image_size

        if image and image.filename != "":

            upload_result = cloudinary.uploader.upload(
                image.file
            )

            product.image = upload_result["secure_url"]

        if video and video.filename != "":

            if product.video != "":

                old_video = f"uploads/videos/{product.video}"

                if os.path.exists(old_video):
                    os.remove(old_video)

            video_path = f"uploads/videos/{video.filename}"

            with open(video_path, "wb") as buffer:
                shutil.copyfileobj(
                    video.file,
                    buffer
                )

            product.video = video.filename

        db.commit()

    db.close()

    return RedirectResponse(
        url="/products",
        status_code=303
    )
@app.get("/delete/{product_id}")
async def delete_product(product_id: int):

    db = SessionLocal()

    product = db.query(Product).filter(
        Product.id == product_id
    ).first()

    if product:

        if product.video != "":

            video_path = f"uploads/videos/{product.video}"

            if os.path.exists(video_path):
                os.remove(video_path)

        db.delete(product)
        db.commit()

    db.close()

    return RedirectResponse(
        url="/products",
        status_code=303
    )
