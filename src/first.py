import os
from dotenv import load_dotenv
load_dotenv()

tst1=os.getenv("API_KEY")
print(tst1)