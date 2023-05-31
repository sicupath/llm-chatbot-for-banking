# AI Virtual Assistant (Hackathon)

## Motivation
We were tasked with creating an AI product for the largest mexican bank (Banorte).\
Modern banking is characterized by an abundance of publicly accessible information. However, this also poses a challenge as clients would have to sift through large quantities of text to find answers to their urgent questions. It can be a time-consuming and sometimes frustrating process. This is where large language models (LLMs) can bridge the gap. Our vision is to further enhance these models by specializing these AI models in the banking domain. By providing them access to extensive banking documents, these AI systems can quickly and accurately draw relevant information to answer clients' queries. 

## What?

We developed a virtual assistant powered by OpenAI's GPT-3.5 model. This assistant has access to a knowledge database created by our team, which contains some of Banorte's most popular products. With this, the assistant can respond to complex, implicitly phrased, poorly structured or grammatically incorrect questions. This gives our solution a significant advantage over traditional virtual assistants.

## Functionality

Our developed Assistant is accesed through Telegram. We imagine this would be a quick and simple way for clients to access.
* The assistant can receive text messages and respond to them using the provided knowledge base.
* The assistant can receive voice messages, transcribe them using Whisper (OpenAI), and respond to them using the provided knowledge base.

## How does it work?

In simple terms, when the assistant receives a message, it searches for relevant information in the provided documents and answers the question using only authorized content.
This task may seem simple, but to make the experience as seamless and effective as possible, some challenges arose. We present them along with their solutions.
1. Challenge: The user's question might be implied from the past conversation.
  * Solution: We store the assistant's conversation with each client in a Redis database (cache type, quick access).
2. Challenge: (Personalization) The agent behaves the same for all profiles regardless of age or background.
  * Solution: We create different agents (assistants) for each profile, where each one has specifications for the type of client they will be working with.
3. Challenge: The client may not have a specifc question. The query could be a more open ended "I need advice" type of query.
  * Solution: The assistant has been programmed to recognize these types of messages, and it will handle the conversation based on the type of client it is interacting with, offering recommendations accordingly.

## Architecture
 <p align="center">
  <img src="https://random-jerry.s3.amazonaws.com/Arq.png" width="900" >
  <img src="https://random-jerry.s3.amazonaws.com/github_images/banorte_infra.png" width="800" >
 </p>

## Activating the Assistant

Create a `.env` file and include the required variables for operation.
```
OPENAI_API_KEY=""
TELEGRAM_TOKEN=""
REDIS_URL=""
```

To spin up the server, we use Docker-compose. This will start the Fastapi server, Nginx, and Redis.
```
docker compose up
```


