from datetime import datetime
x = datetime.now().strftime("%Y-%d-%m")
print(x)
x = datetime.now().strftime("%I.%M.%S%p")
print(x)
