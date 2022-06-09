from fastapi import  FastAPI
from fastapi.responses import HTMLResponse
import random

COUNTER = 0

app = FastAPI()

# catched all urls of pattern http://127.0.0.1:8000/get-links*. 
# example - http://127.0.0.1:8000/get-links123
@app.get("/{xyz}")
async def root() -> dict:
    num_links_each_page = 50
    res = [random.randrange(1, 1000000, 1) for i in range(num_links_each_page)]
    str = " ".join([f"""<li><a href="/get-links{num+random.randint(0,10000)}{num+random.randint(0,10000)}{num+random.randint(0,10000)}{num+random.randint(0,1000)}">{num}</a></li> """ for num in res])

    html_content = f"""
    <html>
        <head>
            <title>Some HTML in here</title>
        </head>
        <body>
            <h1>Links list</h1>
            <ul>
                {str}
            </ul>
        </body>
    </html>
    """
    global COUNTER
    COUNTER += 1
    print(f"total requests received {COUNTER}")
    return HTMLResponse(content=html_content, status_code=200)
