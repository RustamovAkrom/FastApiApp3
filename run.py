import uvicorn

if __name__=='__main__':
    try:
        uvicorn.run("app.main:app", host="127.0.0.0", port=8000, reload=True)

    except KeyboardInterrupt:
        exit(1)