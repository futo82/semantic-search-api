from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI()

# Call openai to create the vector embedding for the text
def get_embedding(text, model="text-embedding-ada-002"):
   text = text.replace("\n", " ")
   return client.embeddings.create(input = [text], model=model).data[0].embedding