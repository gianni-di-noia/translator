from typing import List, Optional

import pymongo
from fastapi import FastAPI, HTTPException, Query, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel

import translator

app = FastAPI()

mongo_client = AsyncIOMotorClient("mongodb://mongo:27017")
db = mongo_client.translations
collection = db.words


class Word(BaseModel):
    word: str
    source_lang: Optional[str]  # TODO: check existance
    target_lang: Optional[str]


class WordDetails(BaseModel):
    word: str
    definitions: Optional[dict] = []
    synonyms: Optional[List[str]] = []
    translations: Optional[dict] = []
    examples: Optional[List[str]] = []


class WordListResponse(BaseModel):
    total: int
    items: List[WordDetails]


@app.post("/word", response_model=WordDetails)
async def add_word(word: Word):
    word_string = word.word.lower()
    existing_word = await collection.find_one({"word": word_string})
    if existing_word:
        existing_word["_id"] = str(existing_word["_id"])
        return JSONResponse(
            content=jsonable_encoder(existing_word), status_code=status.HTTP_200_OK
        )

    fresh_data = translator.translate_word(word_string)
    new_word = {
        "word": word_string,
        "definitions": fresh_data.get("definitions", []),
        "synonyms": fresh_data.get("synonyms", []),
        "translations": fresh_data.get("translations", []),
        "examples": fresh_data.get("examples", []),
    }
    await collection.insert_one(new_word)

    new_word["_id"] = str(new_word["_id"])
    return JSONResponse(content=new_word, status_code=201)


@app.get("/words", response_model=WordListResponse)
async def get_word_list(
    page: int = Query(1, ge=1),
    items_per_page: int = Query(10, ge=1, le=100),
    filter: str = Query("filter", description="Filter criteria"),
    sort_by: str = Query("word", description="Field to sort by"),
    sort_order: str = Query("asc", description="Sort order (asc or desc)"),
    include_definitions: bool = Query(
        False, description="Include definitions in the response"
    ),
    include_synonyms: bool = Query(
        False, description="Include synonyms in the response"
    ),
    include_translations: bool = Query(
        False, description="Include translations in the response"
    ),
):
    # Define sorting order
    sort_order = (
        pymongo.ASCENDING if sort_order.lower() == "asc" else pymongo.DESCENDING
    )

    # Build the filter criteria
    filter_criteria = {}
    if filter:
        filter_criteria["word"] = {"$regex": f".*{filter}.*", "$options": "i"}

    # Count the total number of matching documents
    total = await collection.count_documents(filter_criteria)

    # Fetch the paginated and sorted documents
    words = (
        await collection.find(filter_criteria)
        .sort(sort_by, sort_order)
        .skip((page - 1) * items_per_page)
        .limit(items_per_page)
        .to_list(None)
    )

    # Optionally include definitions, synonyms, and translations
    if not include_definitions:
        for word in words:
            word.pop("definitions", None)
    if not include_synonyms:
        for word in words:
            word.pop("synonyms", None)
    if not include_translations:
        for word in words:
            word.pop("translations", None)

    return WordListResponse(total=total, items=words)


@app.delete("/word/{word}", response_model=dict)
async def delete_word(word: str):
    result = await collection.delete_one({"word": word.lower()})
    if result.deleted_count == 1:
        return {"message": "Word deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Word not found")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)  # type: ignore
