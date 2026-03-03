from RAG.rag import query,BM25Retriever,chunking

with open('transcript.txt','r') as f:
    transcript = f.read()

chunks = chunking(transcript)
bm25 = BM25Retriever(chunks)


# print(transcript)
# print(len(transcript))
while True:
    user_query = input('[USER]: ')
    context = query(transcript,chunks,user_query,bm25)
    for i in context:
        print(i)
    
    print(len(context))
    print('\n')
    print('='*50)
    print('\n')
    
