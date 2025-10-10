from fastapi import FastAPI
#i did import FastAPI from fastapi, so im guessing that's javascript

app = FastAPI()

@app.get('/')
def root():
    return {'message':'Cher Backend'}