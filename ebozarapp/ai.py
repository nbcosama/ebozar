api_gemini = 'AIzaSyByyocXau7I7pyMl2oQVmXfA_ntb9FHeT8'
import google.generativeai as genai
from .models import *


genai.configure(api_key=api_gemini)
model = genai.GenerativeModel("gemini-1.5-flash")


def get_search_results(query):
    products = Product.objects.all()
    prompt_parts = []

    # Build the product list in a cleaner, more compact format.
    for product in products:
        prompt_parts.append(
            f"ID: {product.id}, Name: {product.product_name}, Description: {product.product_description}, "
            f"Brand: {product.brand}, Color: {product.color}, Condition: {product.condtion}, "
            f"Price: {product.price}, Quantity: {product.quantity}, CIty: {product.user.city} Store:  {product.user.store_name}"
        )
    
    # Combine all product information into a single prompt
    product_list = "\n".join(prompt_parts)
    final_prompt = (
        f"You are a search engine for an e-commerce platform. Here are the products in the store:\n\n"
        f"First you need to focus on name. Keyword must be related to name. \n\n"
        f"If You found very unfamilier keyword, done return anything \n\n"
        f"Also if multiple result found, make them assending order based on best matches. \n\n"
        f"If user entered address in keyword, only return the product of that address \n\n"
        f"{product_list}\n\n"
        f"The search keyword is '{query}'. "
        f"Please return only the IDs of the products that match this keyword, separated by commas. "
        f"Do not include any other text or explanations."
    )

    try:
        response = model.generate_content(final_prompt)

        # Attempt to parse the response to ensure it contains only IDs
        response_text = response.text.strip()
        product_ids = [int(id.strip()) for id in response_text.split(",") if id.strip().isdigit()]
        return product_ids
    except ValueError:
        print("Unexpected response format:", response_text)
        return get_search_results(query)


def getSearchFieldSuggestions(query):
    products = Product.objects.all()
    prompt_parts = []

    # Build the product list in a cleaner, more compact format.
    for product in products:
        prompt_parts.append(
            f"ID: {product.id}, Name: {product.product_name}, Description: {product.product_description}, "
            f"Brand: {product.brand}, Color: {product.color}, Condition: {product.condtion}, "
            f"Price: {product.price}, Quantity: {product.quantity}, CIty: {product.user.city} Store:  {product.user.store_name}"
        )
    
    # Combine all product information into a single prompt
    product_list = "\n".join(prompt_parts)
    final_prompt = (
        f"You are a search engine suggestion maker for an e-commerce platform. Here are the products in the store:\n\n"
        f"{product_list}\n\n"
        f"First you need to focus on name. Keyword must be related to name. \n\n"
        f"If You found very unfamilier keyword, done return anything \n\n"
        f"Also if multiple result found, make them assending order based on best matches. \n\n"
        f"If user entered address in keyword, only return the product of that address \n\n"
       
        f"The search keyword is '{query}'. "
        f"Please create some search query suggestions based on this keyword. And return them as a list, separated by commas. follow this pattern: 'keyword1, keyword2, keyword3'. any how follow the patern. complete system is based on this pattern."
        f"If no suggestion found, return null"
       
    )
    try:
        response = model.generate_content(final_prompt)
        response_text = response.text.strip()
        if response_text == "null":
            return []
        lst = response_text.split(",")
        return lst
    except Exception as e:
        print(e)
        return getSearchFieldSuggestions(query)


