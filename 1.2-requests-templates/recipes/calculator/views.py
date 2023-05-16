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
    'salad': {
        'помидор, шт': 2,
        'огурц, шт': 2,
        'укроп, г': 10,
        'масло, г': 10,
        'соль, г': 1
    }
}


def ingredients(request, dish):
    servings_count = int(request.GET.get('servings', 1))
    context = {'recipe': {}}
    for ingredient, count in DATA[dish].items():
        context['recipe'][ingredient] = count * servings_count
    return render(request, 'calculator/index.html', context)
