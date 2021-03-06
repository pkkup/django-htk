ZESTY_URLS = {
    'web_meals' : 'https://meals.zesty.com/clients/%(zesty_id)s/meals',
    'web_meals_today' : 'https://meals.zesty.com/clients/%(zesty_id)s/meals/today',
#    'meals' : 'https://api.zesty.com/portal_api/meals?client_id=%(zesty_id)s',
    'meals' : 'https://api.zesty.com/client_portal_api/meals?client_id=%(zesty_id)s',
    'meal_today' : 'https://api.zesty.com/client_portal_api/meals?client_id=%(zesty_id)s&q=today',
    'meal' : 'https://api.zesty.com/portal_api/meals/%(meal_id)s',
    'dish' : 'https://api.zesty.com/portal_api/dishes/%(dish_id)s',
}
