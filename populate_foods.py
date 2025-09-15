#!/usr/bin/env python
"""
Script para popular o banco de dados com alimentos de exemplo
Execute com: python manage.py shell < populate_foods.py
"""

from inicio.models import Food
import os
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nutra.settings')
django.setup()


# Lista de alimentos com informações nutricionais
foods_data = [
    # Proteínas
    {
        'name': 'Frango (peito)',
        'calories_per_100g': 165,
        'protein_per_100g': 31.0,
        'carbs_per_100g': 0.0,
        'fat_per_100g': 3.6,
        'fiber_per_100g': 0.0,
        'sodium_per_100g': 74,
        'estimated_price': 12.50,
        'category': 'protein'
    },
    {
        'name': 'Ovo (inteiro)',
        'calories_per_100g': 155,
        'protein_per_100g': 12.6,
        'carbs_per_100g': 1.1,
        'fat_per_100g': 11.3,
        'fiber_per_100g': 0.0,
        'sodium_per_100g': 124,
        'estimated_price': 0.80,
        'category': 'protein'
    },
    {
        'name': 'Atum (enlatado)',
        'calories_per_100g': 144,
        'protein_per_100g': 23.4,
        'carbs_per_100g': 0.0,
        'fat_per_100g': 4.9,
        'fiber_per_100g': 0.0,
        'sodium_per_100g': 377,
        'estimated_price': 8.90,
        'category': 'protein'
    },
    {
        'name': 'Carne bovina (patinho)',
        'calories_per_100g': 250,
        'protein_per_100g': 26.0,
        'carbs_per_100g': 0.0,
        'fat_per_100g': 15.0,
        'fiber_per_100g': 0.0,
        'sodium_per_100g': 72,
        'estimated_price': 25.00,
        'category': 'protein'
    },
    {
        'name': 'Queijo cottage',
        'calories_per_100g': 98,
        'protein_per_100g': 11.1,
        'carbs_per_100g': 3.4,
        'fat_per_100g': 4.3,
        'fiber_per_100g': 0.0,
        'sodium_per_100g': 364,
        'estimated_price': 6.50,
        'category': 'dairy'
    },

    # Carboidratos
    {
        'name': 'Arroz branco (cozido)',
        'calories_per_100g': 130,
        'protein_per_100g': 2.7,
        'carbs_per_100g': 28.0,
        'fat_per_100g': 0.3,
        'fiber_per_100g': 0.4,
        'sodium_per_100g': 1,
        'estimated_price': 2.50,
        'category': 'grains'
    },
    {
        'name': 'Batata (cozida)',
        'calories_per_100g': 77,
        'protein_per_100g': 2.0,
        'carbs_per_100g': 17.0,
        'fat_per_100g': 0.1,
        'fiber_per_100g': 2.2,
        'sodium_per_100g': 5,
        'estimated_price': 3.00,
        'category': 'vegetables'
    },
    {
        'name': 'Aveia',
        'calories_per_100g': 389,
        'protein_per_100g': 16.9,
        'carbs_per_100g': 66.3,
        'fat_per_100g': 6.9,
        'fiber_per_100g': 10.6,
        'sodium_per_100g': 2,
        'estimated_price': 4.50,
        'category': 'grains'
    },
    {
        'name': 'Pão integral',
        'calories_per_100g': 247,
        'protein_per_100g': 13.0,
        'carbs_per_100g': 41.0,
        'fat_per_100g': 4.2,
        'fiber_per_100g': 7.0,
        'sodium_per_100g': 400,
        'estimated_price': 8.00,
        'category': 'grains'
    },
    {
        'name': 'Banana',
        'calories_per_100g': 89,
        'protein_per_100g': 1.1,
        'carbs_per_100g': 23.0,
        'fat_per_100g': 0.3,
        'fiber_per_100g': 2.6,
        'sodium_per_100g': 1,
        'estimated_price': 2.00,
        'category': 'fruits'
    },

    # Gorduras
    {
        'name': 'Abacate',
        'calories_per_100g': 160,
        'protein_per_100g': 2.0,
        'carbs_per_100g': 8.5,
        'fat_per_100g': 14.7,
        'fiber_per_100g': 6.7,
        'sodium_per_100g': 7,
        'estimated_price': 4.50,
        'category': 'fruits'
    },
    {
        'name': 'Azeite de oliva',
        'calories_per_100g': 884,
        'protein_per_100g': 0.0,
        'carbs_per_100g': 0.0,
        'fat_per_100g': 100.0,
        'fiber_per_100g': 0.0,
        'sodium_per_100g': 2,
        'estimated_price': 15.00,
        'category': 'fats'
    },
    {
        'name': 'Castanha do Pará',
        'calories_per_100g': 656,
        'protein_per_100g': 14.3,
        'carbs_per_100g': 12.3,
        'fat_per_100g': 66.4,
        'fiber_per_100g': 7.5,
        'sodium_per_100g': 3,
        'estimated_price': 25.00,
        'category': 'fats'
    },

    # Vegetais
    {
        'name': 'Brócolis',
        'calories_per_100g': 34,
        'protein_per_100g': 2.8,
        'carbs_per_100g': 7.0,
        'fat_per_100g': 0.4,
        'fiber_per_100g': 2.6,
        'sodium_per_100g': 33,
        'estimated_price': 5.00,
        'category': 'vegetables'
    },
    {
        'name': 'Espinafre',
        'calories_per_100g': 23,
        'protein_per_100g': 2.9,
        'carbs_per_100g': 3.6,
        'fat_per_100g': 0.4,
        'fiber_per_100g': 2.2,
        'sodium_per_100g': 79,
        'estimated_price': 4.00,
        'category': 'vegetables'
    },
    {
        'name': 'Tomate',
        'calories_per_100g': 18,
        'protein_per_100g': 0.9,
        'carbs_per_100g': 3.9,
        'fat_per_100g': 0.2,
        'fiber_per_100g': 1.2,
        'sodium_per_100g': 5,
        'estimated_price': 3.50,
        'category': 'vegetables'
    },

    # Frutas
    {
        'name': 'Maçã',
        'calories_per_100g': 52,
        'protein_per_100g': 0.3,
        'carbs_per_100g': 14.0,
        'fat_per_100g': 0.2,
        'fiber_per_100g': 2.4,
        'sodium_per_100g': 1,
        'estimated_price': 3.00,
        'category': 'fruits'
    },
    {
        'name': 'Laranja',
        'calories_per_100g': 47,
        'protein_per_100g': 0.9,
        'carbs_per_100g': 12.0,
        'fat_per_100g': 0.1,
        'fiber_per_100g': 2.4,
        'sodium_per_100g': 0,
        'estimated_price': 2.50,
        'category': 'fruits'
    },

    # Laticínios
    {
        'name': 'Leite integral',
        'calories_per_100g': 61,
        'protein_per_100g': 3.2,
        'carbs_per_100g': 4.8,
        'fat_per_100g': 3.3,
        'fiber_per_100g': 0.0,
        'sodium_per_100g': 43,
        'estimated_price': 3.50,
        'category': 'dairy'
    },
    {
        'name': 'Iogurte natural',
        'calories_per_100g': 59,
        'protein_per_100g': 10.0,
        'carbs_per_100g': 3.6,
        'fat_per_100g': 0.4,
        'fiber_per_100g': 0.0,
        'sodium_per_100g': 36,
        'estimated_price': 4.50,
        'category': 'dairy'
    },

    # Outros
    {
        'name': 'Mel',
        'calories_per_100g': 304,
        'protein_per_100g': 0.3,
        'carbs_per_100g': 82.4,
        'fat_per_100g': 0.0,
        'fiber_per_100g': 0.2,
        'sodium_per_100g': 4,
        'estimated_price': 12.00,
        'category': 'other'
    },
    {
        'name': 'Chocolate amargo 70%',
        'calories_per_100g': 598,
        'protein_per_100g': 7.8,
        'carbs_per_100g': 45.5,
        'fat_per_100g': 42.6,
        'fiber_per_100g': 10.9,
        'sodium_per_100g': 20,
        'estimated_price': 18.00,
        'category': 'other'
    }
]


def populate_foods():
    """Popula o banco de dados com alimentos de exemplo"""
    print("Iniciando população do banco de dados com alimentos...")

    # Limpar alimentos existentes (opcional)
    Food.objects.all().delete()
    print("Alimentos existentes removidos.")

    # Criar novos alimentos
    created_count = 0
    for food_data in foods_data:
        try:
            food = Food.objects.create(**food_data)
            created_count += 1
            print(f"Criado: {food.name}")
        except Exception as e:
            print(f"Erro ao criar {food_data['name']}: {e}")

    print(f"\nPopulação concluída! {created_count} alimentos criados.")
    print(f"Total de alimentos no banco: {Food.objects.count()}")


if __name__ == "__main__":
    populate_foods()
