---
title: "Создание вашего первого AI агента: Пошаговое руководство"
date: 2025-09-01T10:00:00+03:00
draft: false
author: "Real AI Engineering"
tags: ["ИИ", "Программирование", "Урок", "Python", "OpenAI"]
categories: ["Уроки"]
description: "Научитесь создавать своего первого AI агента с нуля, используя Python и современные AI фреймворки."
ShowToc: true
TocOpen: false
weight: 2
cover:
    image: ""
    alt: "Создание AI агента"
    caption: "Пошаговое руководство по созданию вашего первого AI агента"
    relative: false
    hidden: true
editPost:
    URL: "https://github.com/Real-AI-Engineering/ai-agents-blog/tree/main/content"
    Text: "Предложить изменения"
    appendFilePath: true
---

## Предварительные требования

Перед началом создания нашего AI агента убедитесь, что у вас есть:
- Python 3.8 или выше
- Базовое понимание программирования на Python
- API ключ OpenAI (для языковой модели)
- Знакомство с интерфейсом командной строки

## Настройка окружения

Сначала создадим новый проект и установим необходимые зависимости:

```bash
mkdir my-first-ai-agent
cd my-first-ai-agent

# Создание виртуального окружения
python -m venv venv
source venv/bin/activate  # На Windows: venv\Scripts\activate

# Установка необходимых пакетов
pip install openai python-dotenv requests beautifulsoup4
```

Создайте файл `.env` для безопасного хранения API ключа:

```env
OPENAI_API_KEY=your_api_key_here
```

## Проектирование нашего AI агента

В этом уроке мы создадим **Агента исследователя**, который может:
1. Принимать тему исследования как входные данные
2. Искать релевантную информацию в интернете
3. Суммировать находки с помощью ИИ
4. Представлять результаты в структурированном формате

## Создание основного класса агента

Начнем с создания базовой структуры агента:

```python
# agent.py
import os
import requests
from bs4 import BeautifulSoup
from openai import OpenAI
from dotenv import load_dotenv
import time
from typing import List, Dict

# Загрузка переменных окружения
load_dotenv()

class ResearchAgent:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.memory = []
        self.tools = {
            "web_search": self.web_search,
            "summarize": self.summarize_content,
            "analyze": self.analyze_information
        }
    
    def perceive(self, user_input: str) -> str:
        """Обработка ввода пользователя и определение необходимого действия"""
        system_prompt = """Вы - агент-помощник исследователь. 
        Получив ввод пользователя, определите, какое действие нужно предпринять.
        Доступные действия: web_search, summarize, analyze
        Верните только название действия."""
        
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_input}
            ],
            temperature=0.1
        )
        
        return response.choices[0].message.content.strip()
    
    def web_search(self, query: str) -> List[str]:
        """Простая функция веб-поиска (макет реализации)"""
        # В реальной реализации вы бы использовали настоящий API поиска
        print(f"🔍 Поиск по запросу: {query}")
        
        # Макет результатов поиска
        mock_results = [
            f"Статья 1 о {query}: Lorem ipsum dolor sit amet...",
            f"Исследовательская работа о {query}: Consectetur adipiscing elit...",
            f"Новостная статья о {query}: Sed do eiusmod tempor..."
        ]
        
        return mock_results
    
    def summarize_content(self, content: List[str]) -> str:
        """Суммирование исследовательского контента с помощью ИИ"""
        combined_content = "\n".join(content)
        
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system", 
                    "content": "Суммируйте следующий контент в ясной, структурированной форме."
                },
                {"role": "user", "content": combined_content}
            ],
            temperature=0.3
        )
        
        return response.choices[0].message.content
    
    def analyze_information(self, summary: str) -> str:
        """Анализ информации и предоставление инсайтов"""
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system", 
                    "content": "Проанализируйте следующую информацию и предоставьте ключевые инсайты, тренды и выводы."
                },
                {"role": "user", "content": summary}
            ],
            temperature=0.4
        )
        
        return response.choices[0].message.content
    
    def act(self, action: str, query: str) -> str:
        """Выполнение определенного действия"""
        if action == "web_search":
            results = self.web_search(query)
            summary = self.summarize_content(results)
            analysis = self.analyze_information(summary)
            
            # Сохранение в памяти
            self.memory.append({
                "query": query,
                "results": results,
                "summary": summary,
                "analysis": analysis,
                "timestamp": time.time()
            })
            
            return f"""
## Результаты исследования по теме: {query}

### Краткое содержание:
{summary}

### Анализ:
{analysis}
            """
        
        return "Запрошено неизвестное действие."
    
    def run(self, user_input: str) -> str:
        """Основной цикл выполнения агента"""
        print(f"🤖 Агент получил: {user_input}")
        
        # Восприятие окружения (ввод пользователя)
        action = self.perceive(user_input)
        print(f"🧠 Агент решил: {action}")
        
        # Действие на основе восприятия
        result = self.act(action, user_input)
        
        return result
```

## Добавление памяти и обучения

Давайте улучшим нашего агента возможностями памяти:

```python
# memory.py
import json
import os
from datetime import datetime

class AgentMemory:
    def __init__(self, memory_file="agent_memory.json"):
        self.memory_file = memory_file
        self.short_term_memory = []
        self.long_term_memory = self.load_memory()
    
    def add_to_memory(self, experience: dict):
        """Добавление нового опыта в память"""
        experience["timestamp"] = datetime.now().isoformat()
        self.short_term_memory.append(experience)
        
        # Перенос в долгосрочную память, если кратковременная заполнена
        if len(self.short_term_memory) > 10:
            self.transfer_to_long_term()
    
    def transfer_to_long_term(self):
        """Перенос опыта в долгосрочную память"""
        self.long_term_memory.extend(self.short_term_memory)
        self.short_term_memory = []
        self.save_memory()
    
    def save_memory(self):
        """Сохранение памяти в файл"""
        with open(self.memory_file, 'w', encoding='utf-8') as f:
            json.dump(self.long_term_memory, f, indent=2, ensure_ascii=False)
    
    def load_memory(self) -> list:
        """Загрузка памяти из файла"""
        if os.path.exists(self.memory_file):
            with open(self.memory_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []
    
    def recall_similar(self, query: str, top_k: int = 3) -> list:
        """Вспоминание похожего прошлого опыта"""
        # Простое сопоставление ключевых слов (в продакшене используйте эмбеддинги)
        relevant_memories = []
        query_words = set(query.lower().split())
        
        for memory in self.long_term_memory:
            memory_words = set(memory.get('query', '').lower().split())
            overlap = len(query_words & memory_words)
            if overlap > 0:
                relevant_memories.append((overlap, memory))
        
        # Возврат топ k наиболее релевантных воспоминаний
        relevant_memories.sort(key=lambda x: x[0], reverse=True)
        return [mem[1] for mem in relevant_memories[:top_k]]
```

## Создание основного приложения

Теперь создадим простой интерфейс для взаимодействия с нашим агентом:

```python
# main.py
from agent import ResearchAgent
from memory import AgentMemory

def main():
    print("🤖 Агент помощник исследователь")
    print("=" * 40)
    
    agent = ResearchAgent()
    memory = AgentMemory()
    
    while True:
        try:
            user_input = input("\n💬 Что вы хотели бы исследовать? (или 'quit' для выхода): ")
            
            if user_input.lower() in ['quit', 'exit', 'q']:
                print("👋 До свидания!")
                break
            
            if not user_input.strip():
                continue
            
            # Проверка на наличие похожих прошлых исследований
            similar_memories = memory.recall_similar(user_input)
            if similar_memories:
                print(f"🧠 Я нашел {len(similar_memories)} похожих прошлых исследований.")
            
            # Обработка запроса
            result = agent.run(user_input)
            print(result)
            
            # Сохранение в память
            memory.add_to_memory({
                "query": user_input,
                "result": result,
                "action_taken": "research"
            })
            
        except KeyboardInterrupt:
            print("\n👋 До свидания!")
            break
        except Exception as e:
            print(f"❌ Ошибка: {e}")

if __name__ == "__main__":
    main()
```

## Тестирование вашего агента

Создадим простой тестовый скрипт:

```python
# test_agent.py
import unittest
from agent import ResearchAgent

class TestResearchAgent(unittest.TestCase):
    def setUp(self):
        self.agent = ResearchAgent()
    
    def test_agent_initialization(self):
        """Тест корректной инициализации агента"""
        self.assertIsNotNone(self.agent.client)
        self.assertIsInstance(self.agent.tools, dict)
        self.assertEqual(len(self.agent.memory), 0)
    
    def test_web_search(self):
        """Тест функциональности веб-поиска"""
        results = self.agent.web_search("искусственный интеллект")
        self.assertIsInstance(results, list)
        self.assertGreater(len(results), 0)
    
    def test_perceive_function(self):
        """Тест функции восприятия"""
        action = self.agent.perceive("Расскажи мне о машинном обучении")
        self.assertIn(action.lower(), ["web_search", "summarize", "analyze"])

if __name__ == '__main__':
    unittest.main()
```

## Запуск вашего агента

Для запуска вашего AI агента:

```bash
# Убедитесь, что ваше виртуальное окружение активировано
source venv/bin/activate

# Запуск агента
python main.py

# Запуск тестов
python test_agent.py
```

## Улучшение вашего агента

Вот несколько способов улучшить вашего агента:

### 1. Добавление дополнительных инструментов
```python
def calculate(self, expression: str) -> str:
    """Функция безопасного калькулятора"""
    try:
        # Используйте eval осторожно в продакшене!
        result = eval(expression)
        return f"Результат: {result}"
    except:
        return "Неверное вычисление"

def get_weather(self, location: str) -> str:
    """Получение информации о погоде (макет)"""
    return f"Погода в {location}: Солнечно, 22°C"
```

### 2. Реализация лучшего поиска
```python
import requests

def real_web_search(self, query: str) -> List[str]:
    """Настоящий веб-поиск используя DuckDuckGo API"""
    url = f"https://api.duckduckgo.com/?q={query}&format=json"
    response = requests.get(url)
    data = response.json()
    
    results = []
    for result in data.get('RelatedTopics', [])[:5]:
        if 'Text' in result:
            results.append(result['Text'])
    
    return results
```

### 3. Добавление истории разговоров
```python
class ConversationAgent(ResearchAgent):
    def __init__(self):
        super().__init__()
        self.conversation_history = []
    
    def run_with_context(self, user_input: str) -> str:
        # Добавление контекста из истории разговоров
        context = "\n".join(self.conversation_history[-5:])  # Последние 5 сообщений
        
        full_input = f"Контекст: {context}\nПользователь: {user_input}"
        result = self.run(full_input)
        
        # Обновление истории разговоров
        self.conversation_history.append(f"Пользователь: {user_input}")
        self.conversation_history.append(f"Агент: {result}")
        
        return result
```

## Лучшие практики

1. **Обработка ошибок**: Всегда обрабатывайте сбои API и сетевые проблемы
2. **Ограничение скорости**: Внедрите задержки между вызовами API
3. **Безопасность**: Никогда не раскрывайте API ключи в коде
4. **Тестирование**: Пишите всесторонние тесты для всех компонентов
5. **Логирование**: Добавьте правильное логирование для отладки и мониторинга

## Заключение

Поздравляем! Вы создали своего первого AI агента. Эта базовая структура может быть расширена с помощью:

- Более сложных возможностей рассуждения
- Интеграции с внешними API и сервисами
- Продвинутых систем памяти
- Сотрудничества множественных агентов
- Веб-интерфейсов или мобильных приложений

Ключ в том, чтобы начать с простого и постепенно добавлять сложность по мере необходимости. Ваш агент станет более мощным и полезным по мере того, как вы продолжите его разрабатывать и совершенствовать.

---

*На следующей неделе мы изучим, как развернуть ваш AI агент в облаке и сделать его доступным через веб-API. Следите за обновлениями!*