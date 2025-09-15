# Sistema de Dieta - Nutra

Este é o sistema de dieta completo para o aplicativo Nutra, implementado com todas as funcionalidades solicitadas baseadas nas imagens de referência.

## ✅ Funcionalidades Implementadas

### 🎯 Metas e Cálculos
- **Meta diária de calorias** calculada automaticamente usando a fórmula de Mifflin-St Jeor
- **Distribuição de macronutrientes** baseada no objetivo (perder, manter ou ganhar peso)
- **Edição manual** de todas as metas nutricionais
- **Cálculo automático** de BMR (Taxa Metabólica Basal)

### 👤 Perfil do Usuário
- Nome completo
- Data de nascimento
- Altura (cm)
- Peso (kg)
- Objetivo: ganhar peso, perder peso ou manter peso
- Metas nutricionais personalizáveis

### 📊 Interface Visual
- **Gráfico circular** mostrando calorias restantes
- **Barras de progresso** para macronutrientes
- **Resumo diário** de calorias consumidas e queimadas
- **Custo diário** da dieta
- **Navegação entre dias** com setas

### 🍽️ Gestão de Refeições
- **Adicionar refeições** com múltiplos alimentos
- **Busca de alimentos** com filtros (Todos, Favoritos, Recentes)
- **Informações nutricionais** completas por 100g
- **Preços estimados** dos alimentos
- **Cálculo automático** de macros por refeição

### 🔄 Funcionalidades Avançadas
- **Copiar refeições** para outros dias
- **Replicar dia completo** para outras datas
- **Limpar dia** (remover todas as refeições)
- **Exportar dieta** (funcionalidade preparada)
- **Editar refeições** (funcionalidade preparada)

## 🚀 Instalação e Configuração

### 1. Migrações do Banco de Dados
```bash
python manage.py makemigrations
python manage.py migrate
```

### 2. Popular Banco com Alimentos
```bash
python manage.py populate_foods
```

### 3. Criar Superusuário (Opcional)
```bash
python manage.py createsuperuser
```

### 4. Executar o Servidor
```bash
python manage.py runserver
```

## 📱 Como Usar

### 1. Configurar Perfil
- Acesse a página de perfil
- Configure seus dados pessoais (altura, peso, objetivo)
- As metas serão calculadas automaticamente

### 2. Usar o Sistema de Dieta
- Acesse a página "Dieta"
- Visualize suas metas diárias no gráfico circular
- Use o botão "+ Adicionar Refeição" para criar refeições
- Navegue entre os dias usando as setas no topo

### 3. Adicionar Refeições
- Clique em "+ Adicionar Refeição"
- Busque alimentos na barra de pesquisa
- Use os filtros para encontrar alimentos específicos
- Selecione alimentos e ajuste as quantidades
- Digite o nome da refeição e salve

### 4. Gerenciar Refeições
- Use "Copiar" para duplicar refeições
- Use "Editar" para modificar refeições existentes
- Use os botões inferiores para ações em lote

## 🗄️ Estrutura do Banco de Dados

### Modelos Principais

#### UserProfile
- Dados pessoais do usuário
- Metas nutricionais
- Cálculos automáticos de BMR

#### Food
- Catálogo de alimentos
- Informações nutricionais por 100g
- Preços estimados
- Categorias para filtros

#### Meal
- Refeições criadas pelo usuário
- Data associada
- Cálculos automáticos de macros

#### MealItem
- Itens individuais em cada refeição
- Quantidades e alimentos específicos

#### DailyNutrition
- Resumo diário de nutrição
- Rastreamento de progresso

## 🔧 APIs Disponíveis

### Perfil
- `POST /api/profile/update/` - Atualizar perfil e metas

### Alimentos
- `GET /api/foods/search/` - Buscar alimentos
- `POST /api/foods/{id}/toggle-favorite/` - Alternar favorito

### Refeições
- `POST /api/meals/add/` - Adicionar refeição
- `DELETE /api/meals/{id}/delete/` - Remover refeição
- `POST /api/meals/{id}/copy/` - Copiar refeição

### Ações em Lote
- `POST /api/diet/clear-day/` - Limpar dia
- `POST /api/diet/replicate-day/` - Replicar dia

## 🎨 Design e Interface

### Características Visuais
- **Tema escuro** consistente com o resto do app
- **Cores verdes** para elementos principais
- **Gradientes** para botões e headers
- **Ícones FontAwesome** para melhor UX
- **Responsivo** para diferentes tamanhos de tela

### Componentes Principais
- Header com navegação de datas
- Card de metas diárias com gráfico circular
- Seção de refeições com cards individuais
- Modais para adicionar/editar refeições
- Botões de ação na parte inferior

## 🔮 Funcionalidades Futuras

### Preparadas para Implementação
- **Edição de refeições** existentes
- **Exportação de dieta** em PDF/Excel
- **Histórico de progresso** com gráficos
- **Sincronização** com dispositivos fitness
- **Receitas** pré-definidas
- **Planejamento semanal** de refeições

### Melhorias Sugeridas
- **Notificações** para lembretes de refeição
- **Integração** com apps de exercício
- **Análise nutricional** avançada
- **Comunidade** para compartilhar refeições
- **IA** para sugestões personalizadas

## 🐛 Solução de Problemas

### Erro de Migração
```bash
python manage.py makemigrations inicio
python manage.py migrate
```

### Erro de Alimentos Vazios
```bash
python manage.py populate_foods
```

### Erro de CSRF
- Verifique se o middleware CSRF está ativo
- Certifique-se de que as requisições incluem o token CSRF

### Erro de Permissões
- Verifique se o usuário está logado
- Confirme que as views têm o decorator `@login_required`

## 📝 Notas Técnicas

### Fórmulas Utilizadas
- **Mifflin-St Jeor** para cálculo de BMR
- **Fatores de atividade** para gasto calórico total
- **Distribuição de macros** baseada em evidências científicas

### Segurança
- Todas as APIs requerem autenticação
- Validação de dados em todos os formulários
- Proteção CSRF em todas as requisições POST

### Performance
- Queries otimizadas para evitar N+1
- Paginação em listas grandes
- Cache de cálculos frequentes

## 🤝 Contribuição

Para contribuir com melhorias:

1. Faça um fork do projeto
2. Crie uma branch para sua feature
3. Implemente as mudanças
4. Teste todas as funcionalidades
5. Envie um pull request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo LICENSE para mais detalhes. 