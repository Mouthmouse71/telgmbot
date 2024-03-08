import os
import openai
import datetime
openai.api_key = "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"
#openai.api_key = os.getenv("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")
#openai.api_key = os.getenv("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") #환경변수로 local에 저장된 api key를 가져오기
#model = "gpt-3"
model = "gpt-3.5-turbo-0301"
     # 모델선택 gpt-4, gpt-4-0314, gpt-4-32k, gpt-4-32k-0314, gpt-3.5-turbo, gpt-3.5-turbo-0301
def Command(Prompt):

  completion = openai.ChatCompletion.create(
    model=model,
    temperature=0,
    messages=[
      {"role": "user", "content": Prompt}
    ]
  )
  result = completion.choices[0]
  message = result.message.content
  print(datetime.datetime.now())
  return message


print("1")