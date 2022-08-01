from unittest import mock
from colorama import Cursor
from flask import Flask, request

from flask import Flask

from about import me

import json

import random

from data import mock_data

from config import db

from bson import ObjectId

from flask_cors import CORS


app = Flask('server')
CORS(app)  # allow request from any origin


@app.get("/")
def home():
    return "Hello from flask server"


@app.get("/test")
def test():
    return "This is just a simple test"

# get /about


@app.get("/about")
def about_me():
    return "My name is Derek"


########################################################
############ API ENDPOINTS = PRODUCTS ##################
########################################################

# get /api/version
# @app.get("/api/version")

@app.get("/api/version")
def version():
    return "1.0"

# create a get request /api/about  and return first name and last name


@app.get("/api/about")
def about_json():

    # return me["first"] + " " + me["last"]

    # return f"{me['first']} {me['last']}"

    return json.dumps(me)  # parse the dicionary into a json string


# get /api/products
# return mock_data as a json string

@app.get("/api/products")
def get_products():
    cursor = db.products.find({})
    results = []
    for prod in cursor:
        fix_mongo_id(prod)
        results.append(prod)
    return json.dumps(results)


def fix_mongo_id(obj):
    obj['id'] = str(obj["_id"])
    del obj["_id"]
    return obj


@app.post("/api/products")
def save_product():
    product = request.get_json()

    db.products.insert_one(product)
    # fix _id
    # product["_id"] = str(product["_id"])
    # del product["_id"]

    # return the product as a json string
    return json.dumps(product)
    return "ok"


@app.get("/api/products/<id>")
def get_products_by_id(id):
    prod = db.products.find_one({"_id": ObjectId(id)})
    if not prod:
        return "ERROR 404"
    fix_mongo_id(prod)
    return json.dumps(prod)

    # travel mock_data list
    # compare the id with id variable
    # if they match, return the product as a json string


## GET /api/categories
# return the list of categories
# 1- return ok
# 2- travel mock_data and print the category of every product
# 3- put the category in a list and at the end of the loop return the list as a json string


@app.get('/api/categories')
def get_categories():
    categories = []
    # for product in mock_data:
    #     cat = product["category"]
    #     if not cat in categories:
    #         categories.append(cat)
    cursor = db.products.find({})
    for product in cursor:
        cat = product["category"]
        if not cat in categories:
            categories.append(cat)

    return json.dumps(categories)

    # GET /api/products_category/<category>
    # return the list of products whose category is the same

    # travel the list and get every prod
    # if prod -> category is equal to the category variable
    # add prod to the results list
    # outside the for loop, return the results list as a json string


@app.get('/api/products_category/<category>')
def get_prods_category(category):
    cursor = db.products.find({"category": category})
    results = []
    for prod in cursor:
        fix_mongo_id(prod)
        results.append(prod)
    return json.dumps(results)

# Get /api/product_cheapest


@app.get('/api/product_cheapest')
def get_cheapest():
    # solution = mock_data[0]
    # for prod in mock_data:
    #     if prod["price"] < solution["price"]:
    #         solution = prod
    # return json.dumps(solution)
    cursor = db.products.find({})
    solution = cursor[0]
    for prod in cursor:
        if prod["price"] < solution["price"]:
            solution = prod
    return json.dumps(solution)


# get endpoint that will return the number of products available in the catalog

# /api/count_products


@app.get('/api/count_products')
def get_count_products():
    count = len(mock_data)
    return json.dumps({"count": count})

# get request /api/search/<text>(<text> is input by the user as the search term)

# return all products whose title contains the search term


@app.get('/api/search/<text>')
def get_search_title(text):
    results = []
    text = text.lower()
    for prod in mock_data:
        if text in prod["title"].lower():
            results.append(prod)

    return json.dumps(results)


app.run(debug=True)
