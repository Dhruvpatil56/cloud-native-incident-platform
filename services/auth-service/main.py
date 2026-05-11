from fastapi import FastAPI
app = FastAPI(title="Auth Service")
@app.get("/health")
async def health(): return {"status": "healthy"}
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002)
