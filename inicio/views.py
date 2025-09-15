from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from django.contrib import messages  # para exibir mensagens (opcional)
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.utils import timezone
from datetime import date, timedelta
import json
import random
import string
import time

from .models import UserProfile, Food, UserFood, Meal, MealItem, DailyNutrition

# Create your views here.


def login(request):
    if request.method == 'POST':
        # Campo ainda se chama 'username' no HTML
        email = request.POST.get('username')
        senha = request.POST.get('senha')

        # Validação básica
        if not email or not senha:
            messages.warning(
                request, "⚠️ Por favor, preencha todos os campos.")
            return render(request, 'login.html')

        # Tentar encontrar o usuário pelo email
        try:
            user = User.objects.get(email=email)
            # Autenticar usando o username do usuário encontrado
            user = authenticate(
                request, username=user.username, password=senha)
        except User.DoesNotExist:
            user = None

        if user is not None:
            auth_login(request, user)
            return redirect('perfil')
        else:
            messages.error(
                request, "❌ Credenciais inválidas! Verifique seu email e senha.")
    return render(request, 'login.html')


def register(request):
    if request.method == 'POST':
        usuario = request.POST.get('usuario')
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        confirma_senha = request.POST.get('confirma-senha')

        if senha != confirma_senha:
            messages.error(request, "As senhas não coincidem.")
            return render(request, 'register.html')

        # Validar força da senha
        if len(senha) < 8:
            messages.error(
                request, "A senha deve ter pelo menos 8 caracteres.")
            return render(request, 'register.html')

        # Verificar se a senha atende aos requisitos mínimos
        has_upper = any(c.isupper() for c in senha)
        has_lower = any(c.islower() for c in senha)
        has_digit = any(c.isdigit() for c in senha)
        has_special = any(c in "!@#$%^&*(),.?\":{}|<>" for c in senha)

        requirements_met = sum([has_upper, has_lower, has_digit, has_special])
        if requirements_met < 3:
            messages.error(
                request, "A senha deve atender aos requisitos mínimos de segurança.")
            return render(request, 'register.html')

        # Verifica se já existe um usuário com este username
        if User.objects.filter(username=usuario).exists():
            messages.error(request, "Nome de usuário já existe.")
            return render(request, 'register.html')

        # Verifica se já existe um usuário com este email
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email já está em uso.")
            return render(request, 'register.html')

        try:
            user = User.objects.create_user(
                username=usuario, email=email, password=senha)
            user.save()
            messages.success(
                request, "Usuário criado com sucesso! Faça login para continuar.")
            return redirect('login')
        except Exception as e:
            messages.error(request, f"Erro ao criar usuário: {e}")

    return render(request, 'register.html')


@login_required
def perfil(request):
    # Obter ou criar perfil do usuário
    profile, created = UserProfile.objects.get_or_create(user=request.user)

    print(f"DEBUG: Carregando perfil para usuário {request.user}")
    print(f"DEBUG: first_name atual: {request.user.first_name}")
    print(f"DEBUG: phone atual: {profile.phone}")

    # Calcular metas apenas se o perfil foi criado agora (não sobrescrever metas existentes)
    if created:
        try:
            profile.daily_calories = profile.calculate_daily_calories()
            protein, carbs, fat = profile.calculate_macros()
            profile.protein_goal = protein
            profile.carbs_goal = carbs
            profile.fat_goal = fat
            profile.save()
        except Exception as e:
            # Se houver erro no cálculo, usar valores padrão
            profile.daily_calories = 2000
            profile.protein_goal = 150
            profile.carbs_goal = 250
            profile.fat_goal = 67
            profile.save()

    return render(request, 'perfil.html', {
        'user': request.user,
        'profile': profile,
        'timestamp': int(time.time())
    })


@login_required
def treino(request):
    return render(request, 'treino.html')


@login_required
def montar_treino(request):
    return render(request, 'montar_treino.html')


@login_required
def configuracoes(request):
    return render(request, 'configuracoes.html')


@login_required
def alterar_senha(request):
    return render(request, 'alterar_senha.html')


@login_required
@csrf_exempt
@require_http_methods(["POST"])
def change_password(request):
    """Altera a senha do usuário"""
    try:
        data = json.loads(request.body)
        current_password = data.get('current_password')
        new_password = data.get('new_password')
        confirm_password = data.get('confirm_password')

        # Validar se a senha atual está correta
        if not request.user.check_password(current_password):
            return JsonResponse({
                'success': False,
                'error': 'Senha atual incorreta'
            })

        # Validar se as novas senhas coincidem
        if new_password != confirm_password:
            return JsonResponse({
                'success': False,
                'error': 'As novas senhas não coincidem'
            })

        # Validar se a nova senha é diferente da atual
        if current_password == new_password:
            return JsonResponse({
                'success': False,
                'error': 'A nova senha deve ser diferente da atual'
            })

        # Alterar a senha
        request.user.set_password(new_password)
        request.user.save()

        # Manter o usuário logado após alterar a senha
        from django.contrib.auth import update_session_auth_hash
        update_session_auth_hash(request, request.user)

        return JsonResponse({
            'success': True,
            'message': 'Senha alterada com sucesso!'
        })

    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


@login_required
@csrf_exempt
@require_http_methods(["POST"])
def update_personal_data(request):
    """Atualiza os dados pessoais do usuário"""
    try:
        print(f"DEBUG: Atualizando dados pessoais para usuário {request.user}")
        print(f"DEBUG: POST data: {request.POST}")

        phone = request.POST.get('phone')
        full_name = request.POST.get('full_name')
        username = request.POST.get('username')

        print(
            f"DEBUG: Phone: '{phone}', Full name: '{full_name}', Username: '{username}'")
        print(
            f"DEBUG: Phone type: {type(phone)}, Phone length: {len(phone) if phone else 0}")

        # Atualizar nome
        if full_name:
            print(f"DEBUG: Atualizando first_name para: {full_name}")
            request.user.first_name = full_name
            request.user.save()
            print(f"DEBUG: first_name salvo: {request.user.first_name}")

        # Atualizar username se fornecido
        if username:
            print(f"DEBUG: Atualizando username para: {username}")
            request.user.username = username
            request.user.save()
            print(f"DEBUG: username salvo: {request.user.username}")

        # Atualizar telefone no perfil
        profile, created = UserProfile.objects.get_or_create(user=request.user)
        print(
            f"DEBUG: Profile criado: {created}, Phone atual: {profile.phone}")

        if phone:
            print(f"DEBUG: Atualizando phone para: '{phone}'")
            profile.phone = phone
        else:
            print(
                f"DEBUG: Phone vazio, mantendo valor atual: '{profile.phone}'")

        profile.save()
        print(f"DEBUG: Profile salvo - phone: '{profile.phone}'")

        # Verificar se foi salvo corretamente
        profile.refresh_from_db()
        print(f"DEBUG: Phone após refresh: '{profile.phone}'")

        return JsonResponse({
            'success': True,
            'message': 'Dados pessoais atualizados com sucesso!',
            'profile': {
                'first_name': request.user.first_name,
                'username': request.user.username,
                'phone': profile.phone
            }
        })

    except Exception as e:
        print(f"DEBUG: Erro ao atualizar dados pessoais: {str(e)}")
        return JsonResponse({'success': False, 'error': str(e)})


@login_required
def sobre_sistema(request):
    return render(request, 'sobre_sistema.html')


@login_required
def sobre_desenvolvedores(request):
    return render(request, 'sobre_desenvolvedores.html')


@login_required
def detalhes_alimento(request, food_id):
    try:
        food = Food.objects.get(id=food_id)
        context = {
            'food': food,
        }
        return render(request, 'detalhes_alimento.html', context)
    except Food.DoesNotExist:
        return redirect('dieta')


@login_required
def dieta(request):
    # Obter ou criar perfil do usuário
    profile, created = UserProfile.objects.get_or_create(user=request.user)

    # Calcular metas apenas se o perfil foi criado agora (não sobrescrever metas existentes)
    if created:
        try:
            profile.daily_calories = profile.calculate_daily_calories()
            protein, carbs, fat = profile.calculate_macros()
            profile.protein_goal = protein
            profile.carbs_goal = carbs
            profile.fat_goal = fat
            profile.save()
        except Exception as e:
            # Se houver erro no cálculo, usar valores padrão
            profile.daily_calories = 2000
            profile.protein_goal = 150
            profile.carbs_goal = 250
            profile.fat_goal = 67
            profile.save()

    # Obter data atual ou da URL
    selected_date = request.GET.get('date', date.today().isoformat())
    try:
        selected_date = date.fromisoformat(selected_date)
    except:
        selected_date = date.today()

    # Obter refeições do dia
    meals = Meal.objects.filter(
        user=request.user, date=selected_date).order_by('created_at')

    # Obter dados nutricionais do dia
    daily_nutrition, created = DailyNutrition.objects.get_or_create(
        user=request.user,
        date=selected_date,
        defaults={
            'calories_consumed': 0,
            'calories_burned': 0,
            'protein_consumed': 0,
            'carbs_consumed': 0,
            'fat_consumed': 0,
            'fiber_consumed': 0,
            'total_cost': 0
        }
    )

    # Calcular totais das refeições com tratamento de erro
    try:
        total_calories = sum(meal.get_total_calories() for meal in meals)
        total_protein = sum(meal.get_total_protein() for meal in meals)
        total_carbs = sum(meal.get_total_carbs() for meal in meals)
        total_fat = sum(meal.get_total_fat() for meal in meals)
        total_fiber = sum(meal.get_total_fiber() for meal in meals)
        total_cost = sum(meal.get_total_cost() for meal in meals)
    except Exception as e:
        # Se houver erro nos cálculos, usar valores padrão
        total_calories = 0
        total_protein = 0
        total_carbs = 0
        total_fat = 0
        total_fiber = 0
        total_cost = 0

    # Atualizar dados diários
    daily_nutrition.calories_consumed = total_calories
    daily_nutrition.protein_consumed = total_protein
    daily_nutrition.carbs_consumed = total_carbs
    daily_nutrition.fat_consumed = total_fat
    daily_nutrition.fiber_consumed = total_fiber
    daily_nutrition.total_cost = total_cost
    daily_nutrition.save()

    context = {
        'profile': profile,
        'meals': meals,
        'selected_date': selected_date,
        'daily_nutrition': daily_nutrition,
        'total_calories': total_calories,
        'total_protein': total_protein,
        'total_carbs': total_carbs,
        'total_fat': total_fat,
        'total_fiber': total_fiber,
        'total_cost': total_cost,
    }

    return render(request, 'dieta.html', context)


@login_required
def adicionar_exercicio(request):
    return render(request, 'adicionar_exercicio.html')


@login_required
def montar_treino_detalhes(request):
    return render(request, 'montar_treino_detalhes.html')


@login_required
def visualizar_treino(request):
    return render(request, 'visualizar_treino.html')


def logout_view(request):
    logout(request)
    # O 'login' aqui é o nome da URL da página de login
    return redirect('login')


# APIs para o sistema de dieta

@login_required
@csrf_exempt
@require_http_methods(["POST"])
def update_profile(request):
    """Atualiza o perfil do usuário"""
    try:
        print(f"DEBUG: Content-Type: {request.content_type}")
        print(f"DEBUG: POST data: {request.POST}")
        print(f"DEBUG: FILES data: {request.FILES}")

        profile, created = UserProfile.objects.get_or_create(user=request.user)

        # Verificar se é um FormData (upload de arquivo) ou JSON
        photo_url = None
        if request.content_type and 'multipart/form-data' in request.content_type:
            # Tratar FormData para upload de foto (se houver)
            if 'profile_photo' in request.FILES and request.FILES['profile_photo']:
                profile_photo = request.FILES['profile_photo']
                print(
                    f"DEBUG: Upload de foto: {profile_photo.name}, tamanho: {profile_photo.size}")
                # Salvar a foto de perfil
                profile.profile_photo = profile_photo
                profile.save()  # Salvar imediatamente para gerar a URL
                photo_url = profile.profile_photo.url if profile.profile_photo else None
                print(f"DEBUG: Foto salva com URL: {photo_url}")
            else:
                print(f"DEBUG: Nenhuma foto enviada")

            # Atualizar campos do perfil
            if 'full_name' in request.POST:
                print(
                    f"DEBUG: Atualizando full_name: {request.POST['full_name']}")
                request.user.first_name = request.POST['full_name']
                request.user.save()

            if 'username' in request.POST:
                print(
                    f"DEBUG: Atualizando username: {request.POST['username']}")
                request.user.username = request.POST['username']
                request.user.save()

            if 'birth_date' in request.POST and request.POST['birth_date']:
                print(
                    f"DEBUG: Atualizando birth_date: {request.POST['birth_date']}")
                from datetime import datetime
                try:
                    birth_date = datetime.strptime(
                        request.POST['birth_date'], '%Y-%m-%d').date()
                    profile.birth_date = birth_date
                except ValueError:
                    print(
                        f"DEBUG: Erro ao converter birth_date: {request.POST['birth_date']}")
                    pass

            if 'gender' in request.POST:
                print(f"DEBUG: Atualizando gender: {request.POST['gender']}")
                profile.gender = request.POST['gender']

            if 'height' in request.POST and request.POST['height']:
                print(f"DEBUG: Atualizando height: {request.POST['height']}")
                try:
                    profile.height = int(request.POST['height'])
                except ValueError:
                    print(
                        f"DEBUG: Erro ao converter height: {request.POST['height']}")
                    pass

            if 'weight' in request.POST and request.POST['weight']:
                print(f"DEBUG: Atualizando weight: {request.POST['weight']}")
                try:
                    profile.weight = float(request.POST['weight'])
                except ValueError:
                    print(
                        f"DEBUG: Erro ao converter weight: {request.POST['weight']}")
                    pass

            if 'objective' in request.POST:
                print(
                    f"DEBUG: Atualizando objective: {request.POST['objective']}")
                profile.objective = request.POST['objective']

            # Processar dados pessoais (telefone apenas - email não pode ser alterado)
            # Email não é processado pois o campo está readonly

            if 'phone' in request.POST:
                profile.phone = request.POST['phone']
        else:
            # Tratar JSON para atualização de metas
            data = json.loads(request.body)

            # Atualizar campos básicos
            if 'first_name' in data:
                request.user.first_name = data['first_name']
                request.user.save()

            if 'birth_date' in data:
                profile.birth_date = data['birth_date']

            if 'height' in data:
                profile.height = data['height']

            if 'weight' in data:
                profile.weight = data['weight']

            if 'objective' in data:
                profile.objective = data['objective']

            # Atualizar metas manualmente se fornecidas
            if 'daily_calories' in data:
                profile.daily_calories = data['daily_calories']

            if 'protein_goal' in data:
                profile.protein_goal = data['protein_goal']

            if 'carbs_goal' in data:
                profile.carbs_goal = data['carbs_goal']

            if 'fat_goal' in data:
                profile.fat_goal = data['fat_goal']

        # Recalcular metas se necessário
        if profile.height and profile.weight and profile.objective:
            profile.daily_calories = profile.calculate_daily_calories()
            protein, carbs, fat = profile.calculate_macros()
            profile.protein_goal = protein
            profile.carbs_goal = carbs
            profile.fat_goal = fat

        print(f"DEBUG: Salvando perfil...")
        print(f"DEBUG: Dados antes do save:")
        print(f"  - first_name: {request.user.first_name}")
        print(f"  - username: {request.user.username}")
        print(f"  - height: {profile.height}")
        print(f"  - weight: {profile.weight}")
        print(f"  - gender: {profile.gender}")
        print(f"  - objective: {profile.objective}")
        print(f"  - birth_date: {profile.birth_date}")

        profile.save()
        request.user.save()
        print(f"DEBUG: Perfil e usuário salvos com sucesso!")

        # Debug: verificar se a foto foi salva
        final_photo_url = None
        if hasattr(profile, 'profile_photo') and profile.profile_photo:
            final_photo_url = profile.profile_photo.url
            print(f"DEBUG: Foto salva com URL: {final_photo_url}")
        elif photo_url:
            final_photo_url = photo_url
            print(f"DEBUG: Foto URL do upload: {final_photo_url}")
        else:
            print(f"DEBUG: Nenhuma foto encontrada")

        return JsonResponse({
            'success': True,
            'message': 'Perfil atualizado com sucesso!',
            'profile': {
                'username': request.user.username,
                'first_name': request.user.first_name,
                'birth_date': profile.birth_date.isoformat() if profile.birth_date else None,
                'height': profile.height,
                'weight': float(profile.weight) if profile.weight else None,
                'objective': profile.objective,
                'daily_calories': profile.daily_calories,
                'protein_goal': profile.protein_goal,
                'carbs_goal': profile.carbs_goal,
                'fat_goal': profile.fat_goal,
                'photo_url': final_photo_url
            }
        })

    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


@login_required
@csrf_exempt
@require_http_methods(["GET"])
def search_foods(request):
    """Busca alimentos"""
    try:
        query = request.GET.get('q', '').lower()
        filter_type = request.GET.get('filter', 'all')

        foods = Food.objects.all()

        # Aplicar filtro de busca
        if query:
            foods = foods.filter(name__icontains=query)

        # Aplicar filtros especiais
        if filter_type == 'favorites':
            try:
                user_foods = UserFood.objects.filter(
                    user=request.user, is_favorite=True)
                foods = foods.filter(userfood__in=user_foods)
            except Exception:
                # Se houver erro, usar todos os alimentos
                pass
        elif filter_type == 'recent':
            try:
                user_foods = UserFood.objects.filter(
                    user=request.user).order_by('-last_used')[:20]
                foods = foods.filter(userfood__in=user_foods)
            except Exception:
                # Se houver erro, usar todos os alimentos
                pass

        # Limitar resultados
        foods = foods[:50]

        food_list = []
        for food in foods:
            try:
                food_list.append({
                    'id': food.id,
                    'name': food.name,
                    'calories_per_100g': food.calories_per_100g,
                    'protein_per_100g': float(food.protein_per_100g),
                    'carbs_per_100g': float(food.carbs_per_100g),
                    'fat_per_100g': float(food.fat_per_100g),
                    'fiber_per_100g': float(food.fiber_per_100g),
                    'sodium_per_100g': food.sodium_per_100g,
                    'estimated_price': float(food.estimated_price),
                    'category': food.category,
                })
            except Exception:
                # Se houver erro com um alimento, pular
                continue

        return JsonResponse({'foods': food_list})
    except Exception as e:
        return JsonResponse({'foods': [], 'error': str(e)})


@login_required
@csrf_exempt
@require_http_methods(["DELETE"])
def delete_meal(request, meal_id):
    """Remove uma refeição"""
    try:
        meal = Meal.objects.get(id=meal_id, user=request.user)
        meal.delete()
        return JsonResponse({'success': True})
    except Meal.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Refeição não encontrada'})


@login_required
@csrf_exempt
@require_http_methods(["GET"])
def get_meal(request, meal_id):
    """Busca dados de uma refeição específica"""
    try:
        meal = Meal.objects.get(id=meal_id, user=request.user)

        # Buscar itens da refeição
        items = []
        for item in meal.mealitem_set.all():
            print(f"DEBUG: Nome do alimento no banco: '{item.food.name}'")

            # Mapear nome do alimento para food_id (string)
            food_name_to_id = {
                'Arroz branco cozido': 'arroz_branco',
                'Feijão carioca cozido': 'feijao_carioca',
                'Peito de frango grelhado': 'peito_frango',
                'Ovo cozido': 'ovo_cozido',
                'Batata doce cozida': 'batata_doce',
                'Banana prata': 'banana_prata',
                'Maçã': 'maca',
                'Brócolis cozido': 'brocolis',
                'Aveia em flocos': 'aveia_flocos',
                'Pão francês': 'pao_frances',
                'Queijo mussarela': 'queijo_mussarela',
                'Leite integral': 'leite_integral',
                'Iogurte natural': 'iogurte_natural',
                'Amêndoas': 'amendoas',
                'Castanha-do-pará': 'castanha_para',
                'Salmão grelhado': 'salmao_grelhado',
                'Carne bovina (patinho)': 'carne_bovina',
                'Quinoa cozida': 'quinoa_cozida',
                'Lentilha cozida': 'lentilha_cozida',
                'Abacate': 'abacate',
            }

            food_id = food_name_to_id.get(
                item.food.name, 'arroz_branco')  # fallback

            print(f"DEBUG: Mapeado para food_id: '{food_id}'")

            items.append({
                'food_id': food_id,
                'quantity': float(item.quantity),
                'food_name': item.food.name
            })

        print(f"DEBUG: Retornando {len(items)} itens para o frontend")
        for item in items:
            print(
                f"DEBUG: Item - food_id: {item['food_id']}, quantity: {item['quantity']}")

        return JsonResponse({
            'success': True,
            'meal': {
                'id': meal.id,
                'name': meal.name,
                'date': meal.date.isoformat(),
                'items': items
            }
        })
    except Meal.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Refeição não encontrada'})


@login_required
@csrf_exempt
@require_http_methods(["PUT"])
def edit_meal(request, meal_id):
    """Edita uma refeição existente"""
    try:
        print(
            f"DEBUG: Editando refeição {meal_id} para usuário {request.user}")

        meal = Meal.objects.get(id=meal_id, user=request.user)

        # Dados do formulário
        meal_name = request.POST.get('meal_name', meal.name)
        foods_json = request.POST.get('foods', '[]')

        print(f"DEBUG: Nome da refeição: {meal_name}")
        print(f"DEBUG: Foods JSON: {foods_json}")

        try:
            foods = json.loads(foods_json)
        except json.JSONDecodeError:
            print("DEBUG: Erro ao fazer parse do JSON")
            return JsonResponse({'success': False, 'error': 'Dados de alimentos inválidos'})

        if not foods:
            print("DEBUG: Nenhum alimento fornecido")
            return JsonResponse({'success': False, 'error': 'Adicione pelo menos um alimento'})

        print(f"DEBUG: {len(foods)} alimentos para processar")

        # Atualizar nome da refeição
        meal.name = meal_name
        meal.save()

        # Remover itens antigos
        meal.mealitem_set.all().delete()
        print("DEBUG: Itens antigos removidos")

        # Adicionar novos itens
        food_data = {
            'arroz_branco': {'name': 'Arroz branco cozido', 'calories': 130, 'protein': 2.5, 'carbs': 28, 'fat': 0.3, 'fiber': 0.4},
            'feijao_carioca': {'name': 'Feijão carioca cozido', 'calories': 77, 'protein': 4.8, 'carbs': 14, 'fat': 0.5, 'fiber': 8.5},
            'peito_frango': {'name': 'Peito de frango grelhado', 'calories': 165, 'protein': 31, 'carbs': 0, 'fat': 3.6, 'fiber': 0},
            'ovo_cozido': {'name': 'Ovo cozido', 'calories': 155, 'protein': 13, 'carbs': 1.1, 'fat': 11, 'fiber': 0},
            'batata_doce': {'name': 'Batata doce cozida', 'calories': 86, 'protein': 1.6, 'carbs': 20, 'fat': 0.1, 'fiber': 2.7},
            'banana_prata': {'name': 'Banana prata', 'calories': 89, 'protein': 1.1, 'carbs': 23, 'fat': 0.3, 'fiber': 2.6},
            'maca': {'name': 'Maçã', 'calories': 52, 'protein': 0.3, 'carbs': 14, 'fat': 0.2, 'fiber': 2.4},
            'brocolis': {'name': 'Brócolis cozido', 'calories': 35, 'protein': 2.4, 'carbs': 7, 'fat': 0.4, 'fiber': 3.3},
            'aveia_flocos': {'name': 'Aveia em flocos', 'calories': 389, 'protein': 16.9, 'carbs': 66, 'fat': 6.9, 'fiber': 8},
            'pao_frances': {'name': 'Pão francês', 'calories': 270, 'protein': 9, 'carbs': 57, 'fat': 3.4, 'fiber': 2.3},
            'queijo_mussarela': {'name': 'Queijo mussarela', 'calories': 280, 'protein': 19, 'carbs': 3, 'fat': 21, 'fiber': 0},
            'leite_integral': {'name': 'Leite integral', 'calories': 61, 'protein': 3.2, 'carbs': 4.8, 'fat': 3.2, 'fiber': 0},
            'iogurte_natural': {'name': 'Iogurte natural', 'calories': 63, 'protein': 3.5, 'carbs': 4.7, 'fat': 3.3, 'fiber': 0},
            'amendoas': {'name': 'Amêndoas', 'calories': 576, 'protein': 21, 'carbs': 22, 'fat': 49, 'fiber': 12.5},
            'castanha_para': {'name': 'Castanha-do-pará', 'calories': 656, 'protein': 14, 'carbs': 12, 'fat': 66, 'fiber': 8.5},
            'salmao_grelhado': {'name': 'Salmão grelhado', 'calories': 208, 'protein': 20, 'carbs': 0, 'fat': 13, 'fiber': 0},
            'carne_bovina': {'name': 'Carne bovina (patinho)', 'calories': 250, 'protein': 26, 'carbs': 0, 'fat': 15, 'fiber': 0},
            'quinoa_cozida': {'name': 'Quinoa cozida', 'calories': 120, 'protein': 4.1, 'carbs': 21, 'fat': 1.9, 'fiber': 2.8},
            'lentilha_cozida': {'name': 'Lentilha cozida', 'calories': 116, 'protein': 9, 'carbs': 20, 'fat': 0.4, 'fiber': 7.9},
            'abacate': {'name': 'Abacate', 'calories': 160, 'protein': 2, 'carbs': 8.5, 'fat': 14.7, 'fiber': 6.7},
        }

        for food_item in foods:
            food_id = food_item['food_id']
            quantity = float(food_item['quantity'])

            if food_id in food_data:
                food_info = food_data[food_id]

                # Criar ou buscar alimento
                food, created = Food.objects.get_or_create(
                    name=food_info['name'],
                    defaults={
                        'calories_per_100g': food_info['calories'],
                        'protein_per_100g': food_info['protein'],
                        'carbs_per_100g': food_info['carbs'],
                        'fat_per_100g': food_info['fat'],
                        'fiber_per_100g': food_info['fiber']
                    }
                )

                # Criar item da refeição
                MealItem.objects.create(
                    meal=meal,
                    food=food,
                    quantity=quantity
                )
                print(
                    f"DEBUG: Criado item - {food_info['name']} ({quantity}g)")

        print("DEBUG: Todos os itens criados com sucesso")
        return JsonResponse({'success': True, 'message': 'Refeição editada com sucesso!'})

    except Meal.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Refeição não encontrada'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': f'Erro interno: {str(e)}'})


@login_required
@csrf_exempt
@require_http_methods(["POST"])
def copy_meal(request, meal_id):
    try:
        data = json.loads(request.body)
        original_meal = Meal.objects.get(id=meal_id, user=request.user)

        # Criar nova refeição
        new_meal = Meal.objects.create(
            user=request.user,
            name=original_meal.name,
            date=data['target_date']
        )

        # Copiar itens
        for item in original_meal.mealitem_set.all():
            MealItem.objects.create(
                meal=new_meal,
                food=item.food,
                quantity=item.quantity
            )

        return JsonResponse({
            'success': True,
            'meal_id': new_meal.id
        })

    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


@login_required
@csrf_exempt
@require_http_methods(["POST"])
def clear_day(request):
    """Limpa todas as refeições de um dia"""
    try:
        data = json.loads(request.body)
        target_date = data['date']

        meals = Meal.objects.filter(user=request.user, date=target_date)
        meals.delete()

        return JsonResponse({'success': True})

    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


@login_required
@csrf_exempt
@require_http_methods(["POST"])
def replicate_day(request):
    """Replica todas as refeições de um dia para outro"""
    try:
        data = json.loads(request.body)
        source_date = data['source_date']
        target_date = data['target_date']

        # Obter refeições do dia fonte
        source_meals = Meal.objects.filter(user=request.user, date=source_date)

        # Copiar para o dia destino
        for meal in source_meals:
            new_meal = Meal.objects.create(
                user=request.user,
                name=meal.name,
                date=target_date
            )

            for item in meal.mealitem_set.all():
                MealItem.objects.create(
                    meal=new_meal,
                    food=item.food,
                    quantity=item.quantity
                )

        return JsonResponse({'success': True})

    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


@login_required
@csrf_exempt
@require_http_methods(["POST"])
def toggle_favorite(request, food_id):
    """Alterna favorito de um alimento"""
    try:
        user_food, created = UserFood.objects.get_or_create(
            user=request.user,
            food_id=food_id
        )
        user_food.is_favorite = not user_food.is_favorite
        user_food.save()

        return JsonResponse({
            'success': True,
            'is_favorite': user_food.is_favorite
        })

    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


def populate_sample_foods(request):
    """Popula o banco com alimentos de exemplo"""
    sample_foods = [
        {
            'name': 'Arroz Branco Cozido',
            'calories_per_100g': 130,
            'protein_per_100g': 2.7,
            'carbs_per_100g': 28.0,
            'fat_per_100g': 0.3,
            'fiber_per_100g': 0.4,
            'sodium_per_100g': 1,
            'estimated_price': 0.50,
            'category': 'cereais'
        },
        {
            'name': 'Frango Grelhado',
            'calories_per_100g': 165,
            'protein_per_100g': 31.0,
            'carbs_per_100g': 0.0,
            'fat_per_100g': 3.6,
            'fiber_per_100g': 0.0,
            'sodium_per_100g': 74,
            'estimated_price': 8.00,
            'category': 'proteinas'
        },
        {
            'name': 'Brócolis',
            'calories_per_100g': 34,
            'protein_per_100g': 2.8,
            'carbs_per_100g': 7.0,
            'fat_per_100g': 0.4,
            'fiber_per_100g': 2.6,
            'sodium_per_100g': 33,
            'estimated_price': 3.50,
            'category': 'vegetais'
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
            'category': 'frutas'
        },
        {
            'name': 'Ovo Cozido',
            'calories_per_100g': 155,
            'protein_per_100g': 13.0,
            'carbs_per_100g': 1.1,
            'fat_per_100g': 11.0,
            'fiber_per_100g': 0.0,
            'sodium_per_100g': 124,
            'estimated_price': 1.50,
            'category': 'proteinas'
        }
    ]

    for food_data in sample_foods:
        Food.objects.get_or_create(
            name=food_data['name'],
            defaults=food_data
        )

    return JsonResponse({'success': True, 'message': 'Alimentos de exemplo adicionados!'})


# Sistema de esqueceu senha
def forgot_password(request):
    """Exibe a página de esqueceu senha"""
    return render(request, 'forgot_password.html')


@require_http_methods(["POST"])
def send_reset_code(request):
    """Envia código de verificação por email"""
    try:
        data = json.loads(request.body)
        email = data.get('email')

        if not email:
            return JsonResponse({
                'success': False,
                'error': 'Email é obrigatório'
            })

        # Verificar se o email existe
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return JsonResponse({
                'success': False,
                'error': 'Email não encontrado em nosso sistema'
            })

        # Gerar código de verificação (6 dígitos)
        code = ''.join(random.choices(string.digits, k=6))

        # Sistema fake - apenas armazenar o código na sessão
        request.session[f'reset_code_{email}'] = code
        request.session[f'reset_code_time_{email}'] = timezone.now(
        ).timestamp()

        # Simular envio de email - retornar o código para exibição na tela
        return JsonResponse({
            'success': True,
            'message': 'Código enviado para seu email!',
            'code': code,  # Para exibição na tela
            'email': email,
            'fake_mode': True  # Indicar que é modo simulado
        })

    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        })


@require_http_methods(["POST"])
def reset_password(request):
    """Redefine a senha do usuário"""
    try:
        data = json.loads(request.body)
        email = data.get('email')
        code = data.get('code')
        new_password = data.get('new_password')

        if not all([email, code, new_password]):
            return JsonResponse({
                'success': False,
                'error': 'Todos os campos são obrigatórios'
            })

        # Verificar código de verificação
        stored_code = request.session.get(f'reset_code_{email}')
        code_time = request.session.get(f'reset_code_time_{email}')

        if not stored_code or not code_time:
            return JsonResponse({
                'success': False,
                'error': 'Código não encontrado ou expirado'
            })

        # Verificar se o código não expirou (15 minutos)
        if timezone.now().timestamp() - code_time > 900:  # 15 minutos
            return JsonResponse({
                'success': False,
                'error': 'Código expirado'
            })

        if stored_code != code:
            return JsonResponse({
                'success': False,
                'error': 'Código de verificação incorreto'
            })

        # Validar força da senha
        if len(new_password) < 8:
            return JsonResponse({
                'success': False,
                'error': 'A senha deve ter pelo menos 8 caracteres'
            })

        # Buscar usuário e alterar senha
        try:
            user = User.objects.get(email=email)
            user.set_password(new_password)
            user.save()

            # Limpar códigos da sessão
            request.session.pop(f'reset_code_{email}', None)
            request.session.pop(f'reset_code_time_{email}', None)

            return JsonResponse({
                'success': True,
                'message': 'Senha redefinida com sucesso!'
            })

        except User.DoesNotExist:
            return JsonResponse({
                'success': False,
                'error': 'Usuário não encontrado'
            })

    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        })


@login_required
@require_http_methods(["POST"])
def update_goals(request):
    """Atualizar metas diárias do usuário"""
    try:
        # Obter ou criar perfil do usuário
        profile, created = UserProfile.objects.get_or_create(user=request.user)

        # Obter dados do formulário
        daily_calories = int(request.POST.get('daily_calories', 2000))
        protein_goal = int(request.POST.get('protein_goal', 150))
        carbs_goal = int(request.POST.get('carbs_goal', 250))
        fat_goal = int(request.POST.get('fat_goal', 67))

        # Validar valores
        if daily_calories < 1000 or daily_calories > 5000:
            return JsonResponse({
                'success': False,
                'error': 'Calorias devem estar entre 1000 e 5000 kcal'
            })

        if protein_goal < 50 or protein_goal > 300:
            return JsonResponse({
                'success': False,
                'error': 'Proteínas devem estar entre 50 e 300g'
            })

        if carbs_goal < 100 or carbs_goal > 500:
            return JsonResponse({
                'success': False,
                'error': 'Carboidratos devem estar entre 100 e 500g'
            })

        if fat_goal < 30 or fat_goal > 150:
            return JsonResponse({
                'success': False,
                'error': 'Gorduras devem estar entre 30 e 150g'
            })

        # Atualizar perfil
        profile.daily_calories = daily_calories
        profile.protein_goal = protein_goal
        profile.carbs_goal = carbs_goal
        profile.fat_goal = fat_goal
        profile.save()

        return JsonResponse({
            'success': True,
            'daily_calories': daily_calories,
            'protein_goal': protein_goal,
            'carbs_goal': carbs_goal,
            'fat_goal': fat_goal
        })

    except ValueError as e:
        return JsonResponse({
            'success': False,
            'error': 'Valores inválidos fornecidos'
        })

    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': f'Erro interno: {str(e)}'
        })


@login_required
@require_http_methods(["POST"])
def add_meal(request):
    """Adicionar nova refeição"""
    try:
        # Obter dados do formulário
        meal_name = request.POST.get('meal_name', '').strip()
        foods_json = request.POST.get('foods', '[]')
        meal_date = request.POST.get('date', date.today().isoformat())

        # Validar dados
        if not meal_name:
            return JsonResponse({
                'success': False,
                'error': 'Nome da refeição é obrigatório'
            })

        try:
            foods = json.loads(foods_json)
        except json.JSONDecodeError:
            return JsonResponse({
                'success': False,
                'error': 'Formato de alimentos inválido'
            })

        if not foods:
            return JsonResponse({
                'success': False,
                'error': 'Adicione pelo menos um alimento'
            })

        # Dados nutricionais dos alimentos (por 100g)
        food_data = {
            'arroz_branco': {'name': 'Arroz branco cozido', 'calories': 130, 'protein': 2.5, 'carbs': 28, 'fat': 0.3, 'fiber': 0.4},
            'feijao_carioca': {'name': 'Feijão carioca cozido', 'calories': 77, 'protein': 4.8, 'carbs': 14, 'fat': 0.5, 'fiber': 8.5},
            'peito_frango': {'name': 'Peito de frango grelhado', 'calories': 165, 'protein': 31, 'carbs': 0, 'fat': 3.6, 'fiber': 0},
            'ovo_cozido': {'name': 'Ovo cozido', 'calories': 155, 'protein': 13, 'carbs': 1.1, 'fat': 11, 'fiber': 0},
            'batata_doce': {'name': 'Batata doce cozida', 'calories': 86, 'protein': 1.6, 'carbs': 20, 'fat': 0.1, 'fiber': 2.7},
            'banana_prata': {'name': 'Banana prata', 'calories': 89, 'protein': 1.1, 'carbs': 23, 'fat': 0.3, 'fiber': 2.6},
            'maca': {'name': 'Maçã', 'calories': 52, 'protein': 0.3, 'carbs': 14, 'fat': 0.2, 'fiber': 2.4},
            'brocolis': {'name': 'Brócolis cozido', 'calories': 35, 'protein': 2.4, 'carbs': 7, 'fat': 0.4, 'fiber': 3.3},
            'aveia_flocos': {'name': 'Aveia em flocos', 'calories': 389, 'protein': 16.9, 'carbs': 66, 'fat': 6.9, 'fiber': 8},
            'pao_frances': {'name': 'Pão francês', 'calories': 270, 'protein': 9, 'carbs': 57, 'fat': 3.4, 'fiber': 2.3},
            'queijo_mussarela': {'name': 'Queijo mussarela', 'calories': 280, 'protein': 19, 'carbs': 3, 'fat': 21, 'fiber': 0},
            'leite_integral': {'name': 'Leite integral', 'calories': 61, 'protein': 3.2, 'carbs': 4.8, 'fat': 3.2, 'fiber': 0},
            'iogurte_natural': {'name': 'Iogurte natural', 'calories': 63, 'protein': 3.5, 'carbs': 4.7, 'fat': 3.3, 'fiber': 0},
            'amendoas': {'name': 'Amêndoas', 'calories': 576, 'protein': 21, 'carbs': 22, 'fat': 49, 'fiber': 12.5},
            'castanha_para': {'name': 'Castanha-do-pará', 'calories': 656, 'protein': 14, 'carbs': 12, 'fat': 66, 'fiber': 8.5},
            'salmao_grelhado': {'name': 'Salmão grelhado', 'calories': 208, 'protein': 20, 'carbs': 0, 'fat': 13, 'fiber': 0},
            'carne_bovina': {'name': 'Carne bovina (patinho)', 'calories': 250, 'protein': 26, 'carbs': 0, 'fat': 15, 'fiber': 0},
            'quinoa_cozida': {'name': 'Quinoa cozida', 'calories': 120, 'protein': 4.1, 'carbs': 21, 'fat': 1.9, 'fiber': 2.8},
            'lentilha_cozida': {'name': 'Lentilha cozida', 'calories': 116, 'protein': 9, 'carbs': 20, 'fat': 0.4, 'fiber': 7.9},
            'abacate': {'name': 'Abacate', 'calories': 160, 'protein': 2, 'carbs': 8.5, 'fat': 14.7, 'fiber': 6.7},
        }

        # Converter data
        try:
            meal_date = date.fromisoformat(meal_date)
        except:
            meal_date = date.today()

        # Criar nova refeição (sempre criar nova)
        meal = Meal.objects.create(
            user=request.user,
            name=meal_name,
            date=meal_date
        )

        # Adicionar cada alimento
        for food_item in foods:
            food_id = food_item.get('food_id')
            quantity = float(food_item.get('quantity', 100))

            if food_id not in food_data:
                continue

            # Obter dados do alimento
            food_info = food_data[food_id]

            # Criar ou obter alimento no banco de dados
            food_obj, food_created = Food.objects.get_or_create(
                name=food_info['name'],
                defaults={
                    'calories_per_100g': food_info['calories'],
                    'protein_per_100g': food_info['protein'],
                    'carbs_per_100g': food_info['carbs'],
                    'fat_per_100g': food_info['fat'],
                    'fiber_per_100g': food_info['fiber'],
                    'estimated_price': 0
                }
            )

            # Criar item da refeição
            MealItem.objects.create(
                meal=meal,
                food=food_obj,
                quantity=quantity
            )

        return JsonResponse({
            'success': True,
            'message': f'Refeição "{meal_name}" adicionada com sucesso!',
            'meal_id': meal.id
        })

    except ValueError as e:
        return JsonResponse({
            'success': False,
            'error': f'Erro de validação: {str(e)}'
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': f'Erro interno: {str(e)}'
        })
