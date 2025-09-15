from django.contrib import admin
from .models import UserProfile, Food, UserFood, Meal, MealItem, DailyNutrition


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'height', 'weight',
                    'objective', 'daily_calories', 'created_at']
    list_filter = ['objective', 'created_at']
    search_fields = ['user__username', 'user__first_name', 'user__last_name']
    readonly_fields = ['created_at', 'updated_at']

    fieldsets = (
        ('Informações do Usuário', {
            'fields': ('user', 'birth_date')
        }),
        ('Medidas', {
            'fields': ('height', 'weight')
        }),
        ('Objetivo', {
            'fields': ('objective',)
        }),
        ('Metas Nutricionais', {
            'fields': ('daily_calories', 'protein_goal', 'carbs_goal', 'fat_goal')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Food)
class FoodAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'calories_per_100g',
                    'protein_per_100g', 'carbs_per_100g', 'fat_per_100g', 'estimated_price']
    list_filter = ['category', 'created_at']
    search_fields = ['name']
    readonly_fields = ['created_at']

    fieldsets = (
        ('Informações Básicas', {
            'fields': ('name', 'category')
        }),
        ('Informações Nutricionais (por 100g)', {
            'fields': ('calories_per_100g', 'protein_per_100g', 'carbs_per_100g', 'fat_per_100g', 'fiber_per_100g', 'sodium_per_100g')
        }),
        ('Preço', {
            'fields': ('estimated_price',)
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )


@admin.register(UserFood)
class UserFoodAdmin(admin.ModelAdmin):
    list_display = ['user', 'food', 'is_favorite', 'last_used']
    list_filter = ['is_favorite', 'last_used']
    search_fields = ['user__username', 'food__name']


@admin.register(Meal)
class MealAdmin(admin.ModelAdmin):
    list_display = ['user', 'name', 'date', 'total_calories',
                    'total_protein', 'total_carbs', 'total_fat', 'created_at']
    list_filter = ['date', 'created_at']
    search_fields = ['user__username', 'name']
    readonly_fields = ['created_at']

    def total_calories(self, obj):
        return obj.get_total_calories()
    total_calories.short_description = 'Calorias Totais'

    def total_protein(self, obj):
        return obj.get_total_protein()
    total_protein.short_description = 'Proteínas (g)'

    def total_carbs(self, obj):
        return obj.get_total_carbs()
    total_carbs.short_description = 'Carboidratos (g)'

    def total_fat(self, obj):
        return obj.get_total_fat()
    total_fat.short_description = 'Gorduras (g)'


@admin.register(MealItem)
class MealItemAdmin(admin.ModelAdmin):
    list_display = ['meal', 'food', 'quantity',
                    'calories', 'protein', 'carbs', 'fat']
    list_filter = ['meal__date']
    search_fields = ['meal__name', 'food__name']

    def calories(self, obj):
        return obj.get_calories()
    calories.short_description = 'Calorias'

    def protein(self, obj):
        return obj.get_protein()
    protein.short_description = 'Proteínas (g)'

    def carbs(self, obj):
        return obj.get_carbs()
    carbs.short_description = 'Carboidratos (g)'

    def fat(self, obj):
        return obj.get_fat()
    fat.short_description = 'Gorduras (g)'


@admin.register(DailyNutrition)
class DailyNutritionAdmin(admin.ModelAdmin):
    list_display = ['user', 'date', 'calories_consumed', 'calories_burned',
                    'protein_consumed', 'carbs_consumed', 'fat_consumed', 'total_cost']
    list_filter = ['date']
    search_fields = ['user__username']
    readonly_fields = ['date']

    fieldsets = (
        ('Usuário e Data', {
            'fields': ('user', 'date')
        }),
        ('Calorias', {
            'fields': ('calories_consumed', 'calories_burned')
        }),
        ('Macronutrientes Consumidos', {
            'fields': ('protein_consumed', 'carbs_consumed', 'fat_consumed', 'fiber_consumed')
        }),
        ('Custo', {
            'fields': ('total_cost',)
        }),
    )
