from django.shortcuts import render
DATA = {
    'omlet': {
        'яйца, шт': 2,
        'молоко, л': 0.1,
        'соль, ч.л.': 0.5,
    },
    'pasta': {
        'макароны, г': 0.3,
        'сыр, г': 0.05,
    },
    'buter': {
        'хлеб, ломтик': 1,
        'колбаса, ломтик': 1,
        'сыр, ломтик': 1,
        'помидор, ломтик': 1,
    },
}

def omlet(request):
    servings = int(request.GET.get('servings', 1))
    adjusted_ingredients = {ingredient: amount * servings for ingredient, amount in DATA['omlet'].items()}
    context = {'ingredients': adjusted_ingredients.items()}
    return render(request, 'calculator/index.html', context)

def pasta(request):
    servings = int(request.GET.get('servings', 1))
    adjusted_ingredients = {ingredient: amount * servings for ingredient, amount in DATA['pasta'].items()}
    context = {'ingredients': adjusted_ingredients.items()}
    return render(request, 'calculator/index.html', context)

def buter(request):
    servings = int(request.GET.get('servings', 1))
    adjusted_ingredients = {ingredient: amount * servings for ingredient, amount in DATA['buter'].items()}
    context = {'ingredients': adjusted_ingredients.items()}
    return render(request, 'calculator/index.html', context)
