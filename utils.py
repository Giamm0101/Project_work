from flask_sqlalchemy import pagination

def paginate_restaurants(restaurants, page):
    per_page = 10  # Adjust the number of accordions per page as needed
    start_index = (page - 1) * per_page
    end_index = start_index + per_page

    paginated_restaurants = restaurants[start_index:end_index]
    return paginated_restaurants