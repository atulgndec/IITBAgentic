#Take a list of ~10 product reviews.
#Concurrently call classify_sentiment on all of them with asyncio.gather (make an async version using aclient).
#Collect the results into a list of Sentiment objects and print a summary: how many positive / neutral / negative, and the average confidence.
#(Stretch) Bound concurrency with a Semaphore, and retry once on ValidationError.

import os
from dotenv import load_dotenv
from pydantic import BaseModel, Field, ValidationError

'''get environ'''
load_dotenv()

test=os.environ.get("OPENROUTER_API_KEY")
BASE_URL = "https://openrouter.ai/api/v1"
DEFAULT_MODEL = "meta-llama/llama-3.3-70b-instruct:free"
STRUCTURED_MODEL = "openai/gpt-4o-mini"
client = OpenAI(base_url=BASE_URL, api_key=API_KEY)

print(test)

prReviews=[
		   'First Review', 'First Review', 'First Review', 'First Review', 'First Review', 
		   'First Review', 'First Review', 'First Review', 'First Review', 'First Review', 
		   ]

class Semantic(BaseModel):
	label: Literal['positive','negative','neutral']
	confidence: float = Field(ge=0, le=1)
	reason: str
	reviews: list[str]


def classify_sentiments(review: str, model: str = STRUCTURED_MODEL) -> Semantic:
	res=client.chat.completions.create(
		model=model,
		messages=[
			{"role":"system","content": "Use a Sentiment Classifier and provide response in JSON format matching the Sentiment Schema"},
			{"role":"user","content": f"classify the sentiment of this review" {review}}
		],
		response_format={

		}


		)
