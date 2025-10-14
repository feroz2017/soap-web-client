# Temperature Conversion REST API

A FastAPI REST API that provides temperature conversion services using the W3Schools SOAP web service behind the scenes.

## Features

- 🚀 **Modern REST Interface**: Clean REST API using FastAPI
- 📚 **Auto-generated Documentation**: Interactive API docs at `/docs`
- 🔄 **Multiple Endpoints**: Both POST and GET endpoints for flexibility
- 📊 **Batch Processing**: REST endpoint for batch conversions
- 🏥 **Health Checks**: Built-in health monitoring
- 🌐 **CORS Support**: Cross-origin resource sharing enabled
- 🌡️ **Temperature Conversion**: Convert between Fahrenheit and Celsius
- 🛡️ **Error Handling**: Robust error handling for network and SOAP faults

## WSDL Service Information

- **Service URL**: https://www.w3schools.com/xml/tempconvert.asmx?WSDL
- **Operations**:
  - `FahrenheitToCelsius`: Convert Fahrenheit to Celsius
  - `CelsiusToFahrenheit`: Convert Celsius to Fahrenheit

## Installation

1. Install required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### REST API Usage

#### Start the API Server

```bash
python3 app.py
```

The API will be available at `http://localhost:8000`

#### API Endpoints

- **GET** `/` - API information
- **GET** `/health` - Health check
- **POST/GET** `/convert/ftc` - Convert Fahrenheit to Celsius
- **POST/GET** `/convert/ctf` - Convert Celsius to Fahrenheit
- **POST** `/convert/batch` - Batch conversion
- **GET** `/docs` - Interactive API documentation

#### Example API Calls

```bash
# Convert Fahrenheit to Celsius (POST)
curl -X POST "http://localhost:8000/convert/ftc" \
     -H "Content-Type: application/json" \
     -d '{"temperature": "32"}'

# Convert Celsius to Fahrenheit (GET)
curl "http://localhost:8000/convert/ctf?temperature=0"

# Batch conversion
curl -X POST "http://localhost:8000/convert/batch" \
     -H "Content-Type: application/json" \
     -d '{"temperatures": ["0", "25", "100"], "from_unit": "celsius"}'

# Health check
curl "http://localhost:8000/health"
```

#### Python API Client Example

```python
import requests

# Convert Fahrenheit to Celsius
response = requests.post("http://localhost:8000/convert/ftc", 
                        json={"temperature": "32"})
result = response.json()
print(f"{result['original']}°F = {result['converted']}°C")

# Batch conversion
response = requests.post("http://localhost:8000/convert/batch",
                        json={"temperatures": ["0", "25", "100"], 
                              "from_unit": "celsius"})
results = response.json()
for result in results['results']:
    print(result)
```

## API Reference

### REST Endpoints

- **GET** `/` - API information and available endpoints
- **GET** `/health` - Health check and service status
- **POST/GET** `/convert/ftc` - Convert Fahrenheit to Celsius
- **POST/GET** `/convert/ctf` - Convert Celsius to Fahrenheit
- **POST** `/convert/batch` - Batch temperature conversion
- **GET** `/docs` - Interactive API documentation (Swagger UI)

## Error Handling

The API handles various types of errors:

- **503 Service Unavailable**: SOAP service not available
- **500 Internal Server Error**: Conversion failures
- **400 Bad Request**: Invalid input parameters
- **404 Not Found**: Endpoint not found

## Deployment

This client can be deployed to various platforms:

### Render (Recommended)
1. Create a new Web Service on Render
2. Connect your GitHub repository
3. Use the included `render.yaml` for automatic configuration
4. Or manually set:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn app:app --host 0.0.0.0 --port $PORT`

### Heroku
1. The `Procfile` is already configured for FastAPI
2. Deploy:
```bash
git push heroku main
```

### Railway
1. Connect your GitHub repository
2. Railway will automatically detect Python and install dependencies
3. The API will be available at the provided URL

### Local Development
```bash
# Install dependencies
pip install -r requirements.txt

# Run the API server
python3 app.py

# Or run with uvicorn directly
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

## Example Output

```
============================================================
🌡️  W3Schools Temperature Conversion SOAP Service
============================================================
📡 Service URL: https://www.w3schools.com/xml/tempconvert.asmx?WSDL
🏷️  Service Name: TempConvert

📋 Available Operations:
   • FahrenheitToCelsius
   • CelsiusToFahrenheit
============================================================

🧪 Testing Single Conversions:
----------------------------------------
✅ 32°F = 0°C
✅ 0°C = 32°F

📊 Testing Batch Conversion:
----------------------------------------
✅ 0°C = 32°F
✅ 25°C = 77°F
✅ 100°C = 212°F

🎯 Interactive Temperature Converter
Commands:
  ftc <temperature>  - Convert Fahrenheit to Celsius
  ctf <temperature>  - Convert Celsius to Fahrenheit
  batch              - Batch conversion mode
  quit               - Exit the program
--------------------------------------------------
```

## Testing

### Manual Testing

1. Start the API server:
```bash
python3 app.py
```

2. Visit the interactive documentation:
   - Open your browser to `http://localhost:8000/docs`
   - Try the API endpoints directly in the browser

3. Test with curl:
```bash
# Health check
curl http://localhost:8000/health

# Convert temperature
curl -X POST "http://localhost:8000/convert/ftc" \
     -H "Content-Type: application/json" \
     -d '{"temperature": "32"}'
```

## Dependencies

- `fastapi`: Modern web framework for building APIs
- `uvicorn`: ASGI server for FastAPI
- `pydantic`: Data validation using Python type annotations
- `zeep`: SOAP client library
- `requests`: HTTP library
- `lxml`: XML processing library

## API Response Examples

### Single Conversion
```json
{
  "original": "32",
  "converted": "0",
  "from_unit": "fahrenheit",
  "to_unit": "celsius"
}
```

### Batch Conversion
```json
{
  "results": [
    "0°C = 32°F",
    "25°C = 77°F",
    "100°C = 212°F"
  ],
  "total_converted": 3,
  "total_errors": 0
}
```

### Health Check
```json
{
  "status": "healthy",
  "soap_service_available": true,
  "version": "1.0.0"
}
```

## License

This project is for educational purposes demonstrating SOAP web service consumption and REST API development.

## Quick Start

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run locally:**
   ```bash
   python3 app.py
   ```

3. **Deploy to Render:**
   - Push to GitHub
   - Connect repository to Render
   - Deploy automatically using `render.yaml`

4. **Access your API:**
   - Local: `http://localhost:8000`
   - Deployed: Your Render URL
   - Documentation: `{your-url}/docs`
