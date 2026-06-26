#Take a list of ~10 product reviews.
#Concurrently call classify_sentiment on all of them with asyncio.gather (make an async version using aclient).
#Collect the results into a list of Sentiment objects and print a summary: how many positive / neutral / negative, and the average confidence.
#(Stretch) Bound concurrency with a Semaphore, and retry once on ValidationError.

import os
from openai import OpenAI
from dotenv import load_dotenv
from pydantic import BaseModel, Field, ValidationError
from typing import Literal


'''get environ'''
load_dotenv()

API_KEY=os.environ.get("OPENROUTER_API_KEY")
BASE_URL = "https://openrouter.ai/api/v1"
DEFAULT_MODEL = "meta-llama/llama-3.3-70b-instruct:free"
STRUCTURED_MODEL = "openai/gpt-4o-mini"
client = OpenAI(base_url=BASE_URL, api_key=API_KEY)

#print(test)

prReviews=[
		   "This product completely exceeded my expectations. The build quality is fantastic, it works flawlessly and customer support was incredibly helpful when I had a question. Would buy again in a heartbeat!",
		   "Absolutely terrible experience. The item arrived broken, customer service was unresponsive for days, and when I finally got a reply they refused to issue a refund. Complete waste of money",
		   "The product does what it says, but nothing special. Shipping took longer than expected and the packaging was a bit flimsy. It's fine for the price, just don't expect anything amazing"
		   ]
# class Sentiment(BaseModel):
#     label: Literal["positive", "neutral", "negative"]
#     confidence: float = Field(ge=0, le=1)
#     reason: str
#     topics: list[str]
#     is_actionable: bool

class Semantic(BaseModel):
	label: Literal["positive","negative","neutral"]
	confidence: float = Field(ge=0, le=1)
	reason: str
	reviews: list[str]


def classify_sentiments(review: str, model: str = STRUCTURED_MODEL) -> Semantic:
	res=client.chat.completions.create(
		model=model,
		messages=[
			{ "role":"system", "content": "Use a Sentiment Classifier and provide response in JSON format matching the Sentiment Schema"},
			{ "role":"user", "content": f"classify the sentiment of this review {review}"}
		],
		response_format={
			"type": "json_schema",
			"json_schema": {"name": "Semantic", "schema": Semantic.model_json_schema()}

		}
		)
	rawout=res.choices[0].message.content
	#print("---------")
#	print(rawout)
	#print("---------")
	return Semantic.model_validate_json(rawout)


result = [ classify_sentiments(i) for i in prReviews ]
for a in result:
	print(a.label,a.confidence,a.reviews)
	print("---------")
#print(result.label,result.confidence)
