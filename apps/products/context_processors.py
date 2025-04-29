from .models import Category  # adjust the import based on your model

def categories_processor(request):
    return {
        'categories': Category.objects.all()
    }
