import requests

indicator = "rsi"
endpoint = f'https://api.taapi.io/{indicator}'
parameters = {
    'secret': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6IndpbHNvbmZvbmc1NkBnbWFpbC5jb20iLCJpYXQiOjE2MjQwNjk0NDAsImV4cCI6NzkzMTI2OTQ0MH0.9_61IM7yiBb8uOcX35ApLkuT9FhGRrihoRaN6XK5eAs',
    'exchange': 'binance',
    'symbol': 'BTC/USDT',
    'interval': '1hr'
    }

response = requests.get(url = endpoint, params = parameters)

result = response.json()

print(result)
