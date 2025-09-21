from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birth_date = models.DateField(null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    height = models.PositiveIntegerField(
        help_text="Altura em cm", null=True, blank=True)
    weight = models.DecimalField(
        max_digits=5, decimal_places=2, help_text="Peso em kg", null=True, blank=True)

    OBJECTIVE_CHOICES = [
        ('lose', 'Perder Peso'),
        ('maintain', 'Manter Peso'),
        ('gain', 'Ganhar Peso'),
    ]
    objective = models.CharField(
        max_length=10, choices=OBJECTIVE_CHOICES, default='maintain')

    GENDER_CHOICES = [
        ('M', 'Masculino'),
        ('F', 'Feminino'),
    ]
    gender = models.CharField(
        max_length=1, choices=GENDER_CHOICES, default='M', help_text="Gênero para cálculos metabólicos")

    # Foto de perfil
    profile_photo = models.ImageField(
        upload_to='profile_photos/',
        null=True,
        blank=True,
        help_text='Foto de perfil do usuário'
    )

    # Metas nutricionais
    daily_calories = models.PositiveIntegerField(default=2000)
    protein_goal = models.PositiveIntegerField(
        default=150, help_text="Proteínas em gramas")
    carbs_goal = models.PositiveIntegerField(
        default=250, help_text="Carboidratos em gramas")
    fat_goal = models.PositiveIntegerField(
        default=67, help_text="Gorduras em gramas")
    fiber_goal = models.PositiveIntegerField(
        default=30, help_text="Fibras em gramas")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Perfil de {self.user.username}"

    def calculate_bmr(self):
        """Calcula o metabolismo basal usando a fórmula de Mifflin-St Jeor"""
        if not self.height or not self.weight:
            return 0

        # Fórmula de Mifflin-St Jeor
        if self.gender == 'F':
            # Mulher
            bmr = 10 * float(self.weight) + 6.25 * \
                self.height - 5 * self.get_age() - 161
        else:
            # Homem (padrão)
            bmr = 10 * float(self.weight) + 6.25 * \
                self.height - 5 * self.get_age() + 5

        return round(bmr)

    def get_age(self):
        """Calcula a idade baseada na data de nascimento"""
        if not self.birth_date:
            return 25  # Idade padrão se não informada
        from datetime import date
        today = date.today()
        return today.year - self.birth_date.year - ((today.month, today.day) < (self.birth_date.month, self.birth_date.day))

    def calculate_daily_calories(self):
        """Calcula as calorias diárias baseadas no objetivo"""
        bmr = self.calculate_bmr()

        # Se não conseguir calcular BMR, usar valor padrão
        if bmr == 0:
            return 2000

        # Fator de atividade (sedentário por padrão)
        activity_factor = 1.2

        # Calorias de manutenção
        maintenance_calories = bmr * activity_factor

        # Ajustar baseado no objetivo
        if self.objective == 'lose':
            return round(maintenance_calories - 500)  # Déficit de 500 calorias
        elif self.objective == 'gain':
            # Superávit de 500 calorias
            return round(maintenance_calories + 500)
        else:
            return round(maintenance_calories)

    def calculate_macros(self):
        """Calcula a distribuição de macronutrientes baseada no objetivo"""
        calories = self.daily_calories

        if self.objective == 'lose':
            # Dieta mais proteica para perda de peso
            protein_ratio = 0.35  # 35% de proteínas
            fat_ratio = 0.30      # 30% de gorduras
            carbs_ratio = 0.35    # 35% de carboidratos
        elif self.objective == 'gain':
            # Dieta mais rica em carboidratos para ganho de peso
            protein_ratio = 0.25  # 25% de proteínas
            fat_ratio = 0.20      # 20% de gorduras
            carbs_ratio = 0.55    # 55% de carboidratos
        else:
            # Dieta equilibrada para manutenção
            protein_ratio = 0.30  # 30% de proteínas
            fat_ratio = 0.25      # 25% de gorduras
            carbs_ratio = 0.45    # 45% de carboidratos

        protein = round((calories * protein_ratio) / 4)  # 4 cal/g de proteína
        fat = round((calories * fat_ratio) / 9)          # 9 cal/g de gordura
        # 4 cal/g de carboidrato
        carbs = round((calories * carbs_ratio) / 4)

        return protein, carbs, fat


class Food(models.Model):
    name = models.CharField(max_length=200)
    calories_per_100g = models.PositiveIntegerField()
    protein_per_100g = models.DecimalField(max_digits=5, decimal_places=2)
    carbs_per_100g = models.DecimalField(max_digits=5, decimal_places=2)
    fat_per_100g = models.DecimalField(max_digits=5, decimal_places=2)
    fiber_per_100g = models.DecimalField(
        max_digits=5, decimal_places=2, default=0)
    sodium_per_100g = models.PositiveIntegerField(
        default=0, help_text="Sódio em mg")
    estimated_price = models.DecimalField(
        max_digits=8, decimal_places=2, default=0, help_text="Preço estimado por 100g")

    # Categorias para filtros
    CATEGORY_CHOICES = [
        ('protein', 'Proteínas'),
        ('carbs', 'Carboidratos'),
        ('fats', 'Gorduras'),
        ('vegetables', 'Vegetais'),
        ('fruits', 'Frutas'),
        ('dairy', 'Laticínios'),
        ('grains', 'Grãos'),
        ('other', 'Outros'),
    ]
    category = models.CharField(
        max_length=20, choices=CATEGORY_CHOICES, default='other')

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class UserFood(models.Model):
    """Alimentos favoritos e recentes do usuário"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    food = models.ForeignKey(Food, on_delete=models.CASCADE)
    is_favorite = models.BooleanField(default=False)
    last_used = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['user', 'food']


class Meal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, default="Refeição")
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.user.username} - {self.date}"

    def get_total_calories(self):
        total = sum(item.get_calories() for item in self.mealitem_set.all())
        return total if total > 0 else 0

    def get_total_protein(self):
        total = sum(item.get_protein() for item in self.mealitem_set.all())
        return total if total > 0 else 0

    def get_total_carbs(self):
        total = sum(item.get_carbs() for item in self.mealitem_set.all())
        return total if total > 0 else 0

    def get_total_fat(self):
        total = sum(item.get_fat() for item in self.mealitem_set.all())
        return total if total > 0 else 0

    def get_total_fiber(self):
        total = sum(item.get_fiber() for item in self.mealitem_set.all())
        return total if total > 0 else 0

    def get_total_cost(self):
        total = sum(item.get_cost() for item in self.mealitem_set.all())
        return total if total > 0 else 0


class MealItem(models.Model):
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE)
    food = models.ForeignKey(Food, on_delete=models.CASCADE)
    quantity = models.DecimalField(
        max_digits=6, decimal_places=2, help_text="Quantidade em gramas")

    def get_calories(self):
        try:
            return round((self.food.calories_per_100g * float(self.quantity)) / 100, 1)
        except:
            return 0

    def get_protein(self):
        try:
            return round((float(self.food.protein_per_100g) * float(self.quantity)) / 100, 1)
        except:
            return 0

    def get_carbs(self):
        try:
            return round((float(self.food.carbs_per_100g) * float(self.quantity)) / 100, 1)
        except:
            return 0

    def get_fat(self):
        try:
            return round((float(self.food.fat_per_100g) * float(self.quantity)) / 100, 1)
        except:
            return 0

    def get_fiber(self):
        try:
            return round((float(self.food.fiber_per_100g) * float(self.quantity)) / 100, 1)
        except:
            return 0

    def get_cost(self):
        try:
            return round((float(self.food.estimated_price) * float(self.quantity)) / 100, 2)
        except:
            return 0


class DailyNutrition(models.Model):
    """Registro diário de nutrição para cálculos de progresso"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    calories_consumed = models.PositiveIntegerField(default=0)
    calories_burned = models.PositiveIntegerField(default=0)
    protein_consumed = models.PositiveIntegerField(default=0)
    carbs_consumed = models.PositiveIntegerField(default=0)
    fat_consumed = models.PositiveIntegerField(default=0)
    fiber_consumed = models.PositiveIntegerField(default=0)
    total_cost = models.DecimalField(max_digits=8, decimal_places=2, default=0)

    class Meta:
        unique_together = ['user', 'date']

    def __str__(self):
        return f"{self.user.username} - {self.date}"
