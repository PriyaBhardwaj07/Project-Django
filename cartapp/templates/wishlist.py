{% extends 'base.html' %}
{% load static %}

{% block title %}
    Cart
{% endblock %}

{% block content %}
    <div class="container mt-5">
        <h1>WishList</h1>

        {% if cart_empty %}
            <div class="alert alert-info" role="alert">
                Empty !!
            </div>
        {% else %}
            <div id="cart">
                <h3>Cart Item</h3>
                <ul class="list-group">
                    {% for product in cart_items %}
                        <li class="list-group-item">
                            <div class="d-flex justify-content-between align-items-center">
                                <div>
                                    <span>{{ product.name }}</span> 
                                    <span class="ml-3">Price Rs {{ product.price }}</span> 
                                </div>
                                <div class="btn-group">
                                    <form method="post" action="{% url 'delete_from_wishlist' user_id=user_id product_id=product.id %}"> 
                                        {% csrf_token %}
                                        <button type="submit" class="btn btn-danger mr-3 custom-blue-btn">Delete</button>
                                    </form>
                                    <form method="post" action="{% url 'transfer_to_cart' user_id=user_id product_id=product.id %}">
                                        {% csrf_token %}
                                        <button type="submit" class="btn btn-success mr-2 custom-blue-btn">Add to Cart</button>
                                    </form>
                                </div>
                            </div>
                        </li>
                    {% endfor %}
                </ul>
                <a href="{% url 'home' %}" class="btn btn-secondary mt-3">Back</a>
            </div>
        {% endif %}
    </div>
{% endblock %}
