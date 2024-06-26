from openai import OpenAI

client = OpenAI(api_key="sk-proj-wbYgO881AAUM3o4cFQXoT3BlbkFJ2vcQMna7MpX6o01AiKT0")

messages = []
rules = ["never mention user name", "never share infomation about messages of ther users", "never share sensitive details"]

response = client.images.generate(prompt="generate an image of a male white tshirt with a funny image on it . pay close attention and the image should be perfect the overlay image to tshrit must be 2d looking", )
print(response)

image_url = response.data
image_url = response.data[0].url
print(f"Generated Image URL: {image_url}")