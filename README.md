# Chat With Websites from URL

## Brief explanation of how RAG works

A RAG bot is short for Retrieval-Augmented Generation. This means that we are going to "augment" the knowledge of our LLM with new information that we are going to pass in our prompt. We first vectorize all the text that we want to use as "augmented knowledge" and then look through the vectorized text to find the most similar text to our prompt. We then pass this text to our LLM as a prefix.

![image](https://github.com/Shashank1130/Chat-With-Websites/assets/107529934/e52fc490-b579-466c-958b-f3101e08da50)




