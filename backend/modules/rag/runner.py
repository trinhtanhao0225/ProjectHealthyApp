# app/modules/rag/runner.py
from backend.modules.rag.data_loader import load_rag_data
from backend.modules.rag.food_database import FoodDatabase
from backend.modules.rag.preprocessor import preprocess_results
from backend.modules.rag.intent_classifier import classify_intent
from backend.modules.rag.prompt_builder import get_prompt, fallback_summary
from backend.modules.rag.llm_generator import generate_stream
from backend.utils.logger import log

def run_food_search(query: str, user_info=None):
    log(f"Starting RAG search for query: {query}")

    food_db = FoodDatabase()

    intent = classify_intent(query)
    log(f"Intent detected: {intent}")

    final_results = []
    if intent != "GENERAL_OTHER":
        results_df = food_db.search_food(query, 60)
        for _, row in results_df.iterrows():
            fdc = row['fdcId']
            details = food_db.get_food_details(fdc)
            ing = food_db.get_ingredients(fdc)
            final_results.append({
                'fdcId': int(fdc),
                'description': row.get('description', str(fdc)),
                'nutrients': details.get('nutrients', {}) if details else {},
                'ingredients': ing
            })

    prepped = preprocess_results(final_results)

    prompt = get_prompt(intent, prepped, query, user_info)

    max_tokens = {
        "PLANNING": 2500,
        "HEALTH_ADVICE": 1500,
        "FOOD_INFO": 1500,
        "GENERAL_OTHER": 800,
        "SEARCH_SUMMARY": 1000
    }.get(intent, 1000)

    summary = generate_stream(prompt, max_tokens=max_tokens)

    if not summary or not summary.strip():
        log("LLM failed → fallback")
        summary = fallback_summary(prepped, query)

    return {
        "status": "success",
        "query": query,
        "summary": summary,
    }