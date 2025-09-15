from django.core.management.base import BaseCommand
from inicio.models import Food


class Command(BaseCommand):
    help = 'Popula o banco de dados com alimentos de exemplo'

    def handle(self, *args, **options):
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

            # Vegetais e Legumes
            {
                'name': 'Cenoura',
                'calories_per_100g': 41,
                'protein_per_100g': 0.9,
                'carbs_per_100g': 9.6,
                'fat_per_100g': 0.2,
                'fiber_per_100g': 2.8,
                'sodium_per_100g': 69,
                'estimated_price': 2.00,
                'category': 'vegetables'
            },
            {
                'name': 'Abobrinha',
                'calories_per_100g': 17,
                'protein_per_100g': 1.2,
                'carbs_per_100g': 3.1,
                'fat_per_100g': 0.3,
                'fiber_per_100g': 1.0,
                'sodium_per_100g': 8,
                'estimated_price': 2.50,
                'category': 'vegetables'
            },
            {
                'name': 'Couve-flor',
                'calories_per_100g': 25,
                'protein_per_100g': 1.9,
                'carbs_per_100g': 5.0,
                'fat_per_100g': 0.3,
                'fiber_per_100g': 2.0,
                'sodium_per_100g': 30,
                'estimated_price': 3.00,
                'category': 'vegetables'
            },
            # Cereais e Grãos
            {
                'name': 'Arroz integral',
                'calories_per_100g': 111,
                'protein_per_100g': 2.6,
                'carbs_per_100g': 23.5,
                'fat_per_100g': 1.0,
                'fiber_per_100g': 1.8,
                'sodium_per_100g': 5,
                'estimated_price': 3.00,
                'category': 'grains'
            },
            {
                'name': 'Quinoa',
                'calories_per_100g': 120,
                'protein_per_100g': 4.4,
                'carbs_per_100g': 21.3,
                'fat_per_100g': 1.9,
                'fiber_per_100g': 2.8,
                'sodium_per_100g': 7,
                'estimated_price': 12.00,
                'category': 'grains'
            },
            {
                'name': 'Milho cozido',
                'calories_per_100g': 96,
                'protein_per_100g': 3.2,
                'carbs_per_100g': 19.0,
                'fat_per_100g': 1.2,
                'fiber_per_100g': 2.7,
                'sodium_per_100g': 15,
                'estimated_price': 2.50,
                'category': 'grains'
            },
            {
                'name': 'Centeio',
                'calories_per_100g': 338,
                'protein_per_100g': 10.3,
                'carbs_per_100g': 75.9,
                'fat_per_100g': 1.6,
                'fiber_per_100g': 15.1,
                'sodium_per_100g': 2,
                'estimated_price': 8.00,
                'category': 'grains'
            },
            # Carnes e Ovos (faltante)
            {
                'name': 'Peixe (tilápia)',
                'calories_per_100g': 96,
                'protein_per_100g': 20.1,
                'carbs_per_100g': 0.0,
                'fat_per_100g': 2.3,
                'fiber_per_100g': 0.0,
                'sodium_per_100g': 50,
                'estimated_price': 10.00,
                'category': 'protein'
            },
            # Oleaginosas e Sementes
            {
                'name': 'Amêndoas',
                'calories_per_100g': 579,
                'protein_per_100g': 21.2,
                'carbs_per_100g': 21.7,
                'fat_per_100g': 49.9,
                'fiber_per_100g': 12.5,
                'sodium_per_100g': 1,
                'estimated_price': 25.00,
                'category': 'nuts'
            },
            {
                'name': 'Nozes',
                'calories_per_100g': 654,
                'protein_per_100g': 15.2,
                'carbs_per_100g': 13.7,
                'fat_per_100g': 65.2,
                'fiber_per_100g': 6.7,
                'sodium_per_100g': 2,
                'estimated_price': 30.00,
                'category': 'nuts'
            },
            {
                'name': 'Chia',
                'calories_per_100g': 486,
                'protein_per_100g': 16.5,
                'carbs_per_100g': 42.1,
                'fat_per_100g': 30.7,
                'fiber_per_100g': 34.4,
                'sodium_per_100g': 16,
                'estimated_price': 18.00,
                'category': 'seeds'
            },
            {
                'name': 'Linhaça',
                'calories_per_100g': 534,
                'protein_per_100g': 18.3,
                'carbs_per_100g': 28.9,
                'fat_per_100g': 42.2,
                'fiber_per_100g': 27.3,
                'sodium_per_100g': 30,
                'estimated_price': 10.00,
                'category': 'seeds'
            },
            # Frutas
            {
                'name': 'Morango',
                'calories_per_100g': 32,
                'protein_per_100g': 0.8,
                'carbs_per_100g': 7.7,
                'fat_per_100g': 0.3,
                'fiber_per_100g': 2.0,
                'sodium_per_100g': 1,
                'estimated_price': 6.00,
                'category': 'fruits'
            },
            {
                'name': 'Mamão',
                'calories_per_100g': 43,
                'protein_per_100g': 0.5,
                'carbs_per_100g': 10.8,
                'fat_per_100g': 0.3,
                'fiber_per_100g': 1.7,
                'sodium_per_100g': 8,
                'estimated_price': 3.00,
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

        self.stdout.write(
            "Iniciando população do banco de dados com alimentos...")

        # Limpar alimentos existentes (opcional)
        Food.objects.all().delete()
        self.stdout.write("Alimentos existentes removidos.")

        # Criar novos alimentos
        created_count = 0
        for food_data in foods_data:
            try:
                food = Food.objects.create(**food_data)
                created_count += 1
                self.stdout.write(f"Criado: {food.name}")
            except Exception as e:
                self.stdout.write(self.style.ERROR(
                    f"Erro ao criar {food_data['name']}: {e}"))

        self.stdout.write(
            self.style.SUCCESS(
                f"\nPopulação concluída! {created_count} alimentos criados.")
        )
        self.stdout.write(
            f"Total de alimentos no banco: {Food.objects.count()}")
