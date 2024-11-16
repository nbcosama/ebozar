from PIL import Image
import io
import json
import os
from dotenv import load_dotenv


api_gemini =  os.getenv("gemin_api")
import google.generativeai as genai
from .models import *

genai.configure(api_key=api_gemini)
model = genai.GenerativeModel("gemini-1.5-flash")


def fallback_search(query, products):
    """
    Fallback search function in case the AI model fails to generate results.
    It performs a simple search within product names and cities based on the query.
    """
    results = []
    for product in products:
        # Perform a basic match on product name or city for the fallback.
        if query.lower() in product.product_name.lower() or query.lower() in product.user.city.lower():
            results.append(product.id)
    return results


def get_search_results(query):
    products = Product.objects.all()
    prompt_parts = []

    # Build the product list in a cleaner, more compact format.
    for product in products:
        prompt_parts.append(
            f"ID: {product.id}, Name: {product.product_name}, Description: {product.product_description}, "
            f"Brand: {product.brand}, Color: {product.color}, Condition: {product.condtion}, "
            f"Price: {product.price}, Quantity: {product.quantity}, City: {product.user.city} Store:  {product.user.store_name}"
        )
    
    # Combine all product information into a single prompt
    product_list = "\n".join(prompt_parts)
    final_prompt = (
        f"You are a search engine for an e-commerce platform. Here are the products in the store:\n\n"
        f"First you need to focus on name. Keyword must be related to name. \n\n"
        f"If You found very unfamiliar keyword, don't return anything \n\n"
        f"Also if multiple results found, make them ascending order based on best matches. \n\n"
        f"If user entered address in keyword, only return the product of that address \n\n"
        f"{product_list}\n\n"
        f"The search keyword is '{query}'. "
        f"Please return only the IDs of the products that match this keyword, separated by commas. "
        f"Do not include any other text or explanations."
    )

    response_text = ""
    try:
        response = model.generate_content(final_prompt)
        response_text = response.text.strip()
        product_ids = [int(id.strip()) for id in response_text.split(",") if id.strip().isdigit()]
        return product_ids
    except Exception as e:
        print("Error occurred:", e)
        print("Fallback triggered due to response error.")
        return fallback_search(query, products)


def getSearchFieldSuggestions(query):
    products = Product.objects.all()
    prompt_parts = []

    # Build the product list in a cleaner, more compact format.
    for product in products:
        prompt_parts.append(
            f"ID: {product.id}, Name: {product.product_name}, Description: {product.product_description}, "
            f"Brand: {product.brand}, Color: {product.color}, Condition: {product.condtion}, "
            f"Price: {product.price}, Quantity: {product.quantity}, City: {product.user.city} Store:  {product.user.store_name}"
        )
    
    # Combine all product information into a single prompt
    product_list = "\n".join(prompt_parts)
    final_prompt = (
        f"You are a search engine suggestion maker for an e-commerce platform. Here are the products in the store:\n\n"
        f"{product_list}\n\n"
        f"First you need to focus on name. Keyword must be related to name. \n\n"
        f"If you found a very unfamiliar keyword, don't return anything \n\n"
        f"Also if multiple results are found, make them ascending order based on best matches. \n\n"
        f"If user entered address in keyword, only return the product of that address \n\n"
       
        f"The search keyword is '{query}'. "
        f"Please create some search query suggestions based on this keyword. Return them as a list, separated by commas in this pattern: 'keyword1, keyword2, keyword3'. "
        f"If no suggestion is found, return 'null'."
    )

    response_text = ""
    try:
        response = model.generate_content(final_prompt)
        response_text = response.text.strip()
        if response_text == "null":
            return []
        return response_text.split(",")
    except Exception as e:
        print("Error occurred:", e)
        print("Fallback triggered for suggestions.")
        return []



def productDetailLoader(request):
    print("yes")
    print("Files in request:", request.FILES.get("image"))
    if request.method == "POST" and request.FILES.get("image"):
        img = request.FILES["image"]
        image = Image.open(img)
        buffer = io.BytesIO()
        image.save(buffer, format="JPEG")
        buffer.seek(0)

        try:
            # Upload the file using genai (ensure `upload_file` works with Django's `UploadedFile` or convert as needed)
            myfile = genai.upload_file(buffer, mime_type="image/jpeg")
            model = genai.GenerativeModel("gemini-1.5-flash")
            result = model.generate_content(
                [
                    myfile,
                    "\n\n",
                    "Provide product details with the following JSON structure:",
                    '{"product": "product name", "price": "price range or estimate", "color": "primary colors", "condition": "new or used", "description": "brief product description", "brand": "", "quantity": ""}',
                    "Avoid adding extra text, do not use double quotes around keys or values, and follow this structure strictly."
                    "price must be in nepali rupees. only use single number"
                    "only one price expected. dont put Rs. if unknown price return 0. But do your best to guess the price."
                    "if no brand found, return unknown"
                    "for quantity, products that comes in pair, if one pair found return 1, and try to count number of product in image."
                    "for color only return one main primary color."
                    "in descrption try to put all color. make it seo friendly."
                    "make the title eye catchy and SEO Friendly"
                    "strictly follow the structure."
                    "avoid ```json from start and ``` in end. just start from '{ and end in }'"
                ]
            )

            print(result.text)
            data = json.loads(result.text)
            # Further processing can be done here with `myfile`
            return {"status": "success", "data": data}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    return {"status": "error", "message": "Invalid request"} 
