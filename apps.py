from fastapi import FastAPI, Request, Form, UploadFile, File
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
import shutil
import os

from database import engine, SessionLocal

from models.product import Product
from models.category import Category
from models.review import Review


app = FastAPI()


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


@app.get("/")
async def home(request: Request):

    db = SessionLocal()

    products = db.query(Product).all()

    featured_products = db.query(Product).filter(
        Product.featured == True
    ).all()

    categories = db.query(Category).all()

    db.close()

    return templates.TemplateResponse(
        request=request,
        name="D_ultimat.html",
        context={
            "products": products,
            "featured_products": featured_products,
            "categories": categories
        }
    )


@app.get("/admin")
async def admin(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="admin_login.html"
    )


@app.post("/admin")
async def admin_login(
    username: str = Form(...),
    password: str = Form(...)
):

    if (
        username == "Ruvira"
        and
        password == "Ruvira@2007"
    ):

        return RedirectResponse(
            url="/dashboard",
            status_code=303
        )

    return RedirectResponse(
        url="/admin",
        status_code=303
    )


@app.get("/dashboard")
async def dashboard(request: Request):

    db = SessionLocal()

    total_products = db.query(Product).count()

    total_reviews = db.query(Review).count()

    featured_count = db.query(Product).filter(
        Product.featured == True
    ).count()

    db.close()

    return templates.TemplateResponse(
        request=request,
        name="dashboard.html",
        context={
            "total_products": total_products,
            "total_reviews": total_reviews,
            "featured_count": featured_count
        }
    )
@app.get("/add-product")
async def add_product(request: Request):

    db = SessionLocal()

    categories = db.query(Category).all()

    db.close()

    return templates.TemplateResponse(
        request=request,
        name="add_product.html",
        context={
            "categories": categories
        }
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

    image_path = f"uploads/{image.filename}"

    with open(image_path, "wb") as buffer:
        shutil.copyfileobj(
            image.file,
            buffer
        )

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
        image=image.filename,
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


@app.get("/products")
async def products(
    request: Request,
    search: str = "",
    category: str = ""
):

    db = SessionLocal()

    query = db.query(Product)

    if search:

        query = query.filter(
            Product.name.contains(search)
        )

    if category:

        query = query.filter(
            Product.category == category
        )

    all_products = query.all()

    categories = db.query(Category).all()

    db.close()

    return templates.TemplateResponse(
        request=request,
        name="product_list.html",
        context={
            "products": all_products,
            "search": search,
            "category": category,
            "categories": categories
        }
    )


@app.get("/product/{product_id}")
async def product_detail(
    request: Request,
    product_id: int
):

    db = SessionLocal()

    product = db.query(Product).filter(
        Product.id == product_id
    ).first()

    reviews = db.query(Review).filter(
        Review.product_id == product_id
    ).all()

    related_products = db.query(Product).filter(
        Product.category == product.category
    ).all()

    db.close()

    return templates.TemplateResponse(
        request=request,
        name="product_detail.html",
        context={
            "product": product,
            "reviews": reviews,
            "related_products": related_products
        }
    )
@app.get("/edit/{product_id}")
async def edit_product(
    product_id: int,
    request: Request
):

    db = SessionLocal()

    product = db.query(Product).filter(
        Product.id == product_id
    ).first()

    categories = db.query(Category).all()

    db.close()

    return templates.TemplateResponse(
        request=request,
        name="edit_product.html",
        context={
            "product": product,
            "categories": categories
        }
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

            old_image = f"uploads/{product.image}"

            if os.path.exists(old_image):
                os.remove(old_image)

            image_path = f"uploads/{image.filename}"

            with open(image_path, "wb") as buffer:
                shutil.copyfileobj(
                    image.file,
                    buffer
                )

            product.image = image.filename

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

        image_path = f"uploads/{product.image}"

        if os.path.exists(image_path):
            os.remove(image_path)

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


@app.get("/categories")
async def categories_page(request: Request):

    db = SessionLocal()

    categories = db.query(Category).all()

    db.close()

    return templates.TemplateResponse(
        request=request,
        name="manage_categories.html",
        context={
            "categories": categories
        }
    )


@app.post("/add-category")
async def add_category(
    category_name: str = Form(...)
):

    db = SessionLocal()

    category = Category(
        name=category_name
    )

    db.add(category)
    db.commit()
    db.close()

    return RedirectResponse(
        url="/categories",
        status_code=303
    )
@app.post("/add-review/{product_id}")
async def add_review(
    product_id: int,
    customer_name: str = Form(...),
    rating: int = Form(...),
    comment: str = Form(...)
):

    db = SessionLocal()

    review = Review(
        customer_name=customer_name,
        rating=rating,
        comment=comment,
        product_id=product_id
    )

    db.add(review)
    db.commit()
    db.close()

    return RedirectResponse(
        url=f"/product/{product_id}",
        status_code=303
    )


@app.get("/analytics")
async def analytics(request: Request):

    db = SessionLocal()

    total_products = db.query(Product).count()

    total_reviews = db.query(Review).count()

    total_categories = db.query(Category).count()

    db.close()

    return templates.TemplateResponse(
        request=request,
        name="analytics.html",
        context={
            "total_products": total_products,
            "total_reviews": total_reviews,
            "total_categories": total_categories
        }
    )


@app.get("/about")
async def about_page(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="about.html"
    )


@app.get("/contact")
async def contact_page(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="contact.html"
    )


@app.get("/faq")
async def faq_page(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="faq.html"
    )


@app.get("/privacy-policy")
async def privacy_policy(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="privacy_policy.html"
    )


@app.get("/return-policy")
async def return_policy(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="return_policy.html"
    )


@app.get("/terms")
async def terms_page(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="terms.html"
    )
@app.get("/featured-products")
async def featured_products(request: Request):

    db = SessionLocal()

    featured = db.query(Product).filter(
        Product.featured == True
    ).all()

    db.close()

    return templates.TemplateResponse(
        request=request,
        name="featured_products.html",
        context={
            "products": featured
        }
    )


@app.post("/make-featured/{product_id}")
async def make_featured(product_id: int):

    db = SessionLocal()

    product = db.query(Product).filter(
        Product.id == product_id
    ).first()

    if product:

        product.featured = True

        db.commit()

    db.close()

    return RedirectResponse(
        url="/products",
        status_code=303
    )


@app.post("/remove-featured/{product_id}")
async def remove_featured(product_id: int):

    db = SessionLocal()

    product = db.query(Product).filter(
        Product.id == product_id
    ).first()

    if product:

        product.featured = False

        db.commit()

    db.close()

    return RedirectResponse(
        url="/products",
        status_code=303
    )


@app.get("/home-products")
async def home_products(request: Request):

    db = SessionLocal()

    products = db.query(Product).all()

    db.close()

    return templates.TemplateResponse(
        request=request,
        name="D_ultimat.html",
        context={
            "products": products
        }
    )


@app.get("/health")
async def health_check():

    return {
        "status": "running",
        "project": "Ruvira Jewellery"
    }