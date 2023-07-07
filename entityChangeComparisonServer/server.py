from fastapi import FastAPI


app = FastAPI()

@app.post("/v6/entity-change-comparison/{tenant}/{source_id}")
def change_comparison():
    pass