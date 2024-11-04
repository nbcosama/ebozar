# api_gemini = 'AIzaSyByyocXau7I7pyMl2oQVmXfA_ntb9FHeT8'
# import google.generativeai as genai
# from .models import *


# genai.configure(api_key=api_gemini)
# model = genai.GenerativeModel("gemini-1.5-flash")


# def get_search_results(query):
#     products = Product.objects.all()
#     prompt_parts = []

#     # Build the product list in a cleaner, more compact format.
#     for product in products:
#         prompt_parts.append(
#             f"ID: {product.id}, Name: {product.product_name}, Description: {product.product_description}, "
#             f"Brand: {product.brand}, Color: {product.color}, Condition: {product.condtion}, "
#             f"Price: {product.price}, Quantity: {product.quantity}, CIty: {product.user.city} Store:  {product.user.store_name}"
#         )
    
#     # Combine all product information into a single prompt
#     product_list = "\n".join(prompt_parts)
#     final_prompt = (
#         f"You are a search engine for an e-commerce platform. Here are the products in the store:\n\n"
#         f"First you need to focus on name. Keyword must be related to name. \n\n"
#         f"If You found very unfamilier keyword, done return anything \n\n"
#         f"Also if multiple result found, make them assending order based on best matches. \n\n"
#         f"If user entered address in keyword, only return the product of that address \n\n"
#         f"{product_list}\n\n"
#         f"The search keyword is '{query}'. "
#         f"Please return only the IDs of the products that match this keyword, separated by commas. "
#         f"Do not include any other text or explanations."
#     )

#     try:
#         response = model.generate_content(final_prompt)

#         # Attempt to parse the response to ensure it contains only IDs
#         response_text = response.text.strip()
#         product_ids = [int(id.strip()) for id in response_text.split(",") if id.strip().isdigit()]
#         return product_ids
#     except ValueError:
#         print("Unexpected response format:", response_text)
#         return get_search_results(query)


# def getSearchFieldSuggestions(query):
#     products = Product.objects.all()
#     prompt_parts = []

#     # Build the product list in a cleaner, more compact format.
#     for product in products:
#         prompt_parts.append(
#             f"ID: {product.id}, Name: {product.product_name}, Description: {product.product_description}, "
#             f"Brand: {product.brand}, Color: {product.color}, Condition: {product.condtion}, "
#             f"Price: {product.price}, Quantity: {product.quantity}, CIty: {product.user.city} Store:  {product.user.store_name}"
#         )
    
#     # Combine all product information into a single prompt
#     product_list = "\n".join(prompt_parts)
#     final_prompt = (
#         f"You are a search engine suggestion maker for an e-commerce platform. Here are the products in the store:\n\n"
#         f"{product_list}\n\n"
#         f"First you need to focus on name. Keyword must be related to name. \n\n"
#         f"If You found very unfamilier keyword, done return anything \n\n"
#         f"Also if multiple result found, make them assending order based on best matches. \n\n"
#         f"If user entered address in keyword, only return the product of that address \n\n"
       
#         f"The search keyword is '{query}'. "
#         f"Please create some search query suggestions based on this keyword. And return them as a list, separated by commas. follow this pattern: 'keyword1, keyword2, keyword3'. any how follow the patern. complete system is based on this pattern."
#         f"If no suggestion found, return null"
       
#     )
#     try:
#         response = model.generate_content(final_prompt)
#         response_text = response.text.strip()
#         if response_text == "null":
#             return []
#         lst = response_text.split(",")
#         return lst
#     except Exception as e:
#         print(e)
#         return getSearchFieldSuggestions(query)









api_gemini = 'AIzaSyByyocXau7I7pyMl2oQVmXfA_ntb9FHeT8'
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
