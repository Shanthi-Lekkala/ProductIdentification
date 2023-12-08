import openfoodfacts

def get_ingredients(ingred):
    new_ingred = {}
    for i in range(len(ingred)):
        new_d = {}
        d = ingred[i]
        if d['id']: id = d['id'].split(':')[1]
        if 'percent_estimate' in d: new_d['percent_estimate'] = d['percent_estimate']
        if 'percent_max' in d : new_d['percent_max'] = d['percent_max']
        if 'percent_min' in d: new_d['percent_min'] = d['percent_min']

        new_ingred[id] = new_d

    return new_ingred

def get_nutrient_table(nutrients):
    nutrient_table = {}
    for i in nutrients:
        d = i.split('_')
        id = d[0]
        if id not in nutrient_table: nutrient_table[id] = {}
        if len(d)==2: nutrient_table[id][d[1]] = nutrients[i]

    return nutrient_table

def get_allergens(allergens):
    return [word.split(':')[1] for word in allergens]

def get_brand(response):
    if 'brands' in response: return response['brands']
    if 'brand_owner' in response: return response['brand_owner']
    return ''

def get_product_json(barcode):
	api = openfoodfacts.API(version="v2")
	response = api.product.get(barcode)['product']

	product_info = {}
	product_info['id'] = barcode
	product_info['name'] = response['product_name'] if 'product_name' in response else ''
	product_info['nutrients'] = get_nutrient_table(response['nutriments']) if 'nutriments' in response else ''
	product_info['ingredients'] = get_ingredients(response['ingredients']) if 'ingredients' in response else ''
	product_info['allergens'] = get_allergens(response['allergens_hierarchy']) if 'allergens_hierarchy' in response else ''
	product_info['labels'] = response['labels'] if 'labels' in response else ''
	product_info['packaging'] = response['packaging'] if 'packaging' in response else ''
	product_info['brand_owner'] = get_brand(response)
	product_info['serving_size'] = response['serving_size'] if 'serving_size' in response else ''

	return product_info

if __name__ == '__main__':
	barcode = "016000124790"
	print(get_product_json(barcode))