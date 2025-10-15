#!/usr/bin/env python3
"""
FastAPI REST Interface for SOAP Temperature Conversion Service
This provides a REST API wrapper around the W3Schools SOAP temperature conversion service.
"""

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional
from contextlib import asynccontextmanager
import logging
from zeep import Client, Settings
from zeep.exceptions import Fault, TransportError

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize SOAP client
soap_client = None

class TemperatureConverterClient:
    """Simple SOAP client for temperature conversion"""
    
    def __init__(self, wsdl_url="https://www.w3schools.com/xml/tempconvert.asmx?WSDL"):
        settings = Settings(strict=False, xml_huge_tree=True)
        self.client = Client(wsdl_url, settings=settings)
    
    def fahrenheit_to_celsius(self, fahrenheit):
        """Convert Fahrenheit to Celsius"""
        return self.client.service.FahrenheitToCelsius(Fahrenheit=fahrenheit)
    
    def celsius_to_fahrenheit(self, celsius):
        """Convert Celsius to Fahrenheit"""
        return self.client.service.CelsiusToFahrenheit(Celsius=celsius)
    
    def batch_conversion(self, temperatures, from_unit='celsius'):
        """Convert multiple temperatures"""
        results = []
        for temp in temperatures:
            try:
                if from_unit.lower() == 'celsius':
                    converted = self.celsius_to_fahrenheit(str(temp))
                    results.append(f"{temp}°C = {converted}°F")
                else:
                    converted = self.fahrenheit_to_celsius(str(temp))
                    results.append(f"{temp}°F = {converted}°C")
            except Exception as e:
                results.append(f"Error converting {temp}: {e}")
        return results

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize and cleanup resources"""
    global soap_client
    try:
        soap_client = TemperatureConverterClient()
        logger.info("SOAP client initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize SOAP client: {e}")
        raise
    yield
    # Cleanup if needed
    logger.info("Shutting down...")

# Initialize FastAPI app
app = FastAPI(
    title="Temperature Conversion API",
    description="REST API wrapper for W3Schools SOAP Temperature Conversion Service",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models for request/response
class TemperatureRequest(BaseModel):
    temperature: str = Field(..., description="Temperature value to convert", example="32")
    
class TemperatureResponse(BaseModel):
    original: str = Field(..., description="Original temperature value")
    converted: str = Field(..., description="Converted temperature value")
    from_unit: str = Field(..., description="Source temperature unit")
    to_unit: str = Field(..., description="Target temperature unit")
    
class BatchConversionRequest(BaseModel):
    temperatures: List[str] = Field(..., description="List of temperatures to convert", example=["0", "25", "100"])
    from_unit: str = Field(..., description="Source unit (celsius or fahrenheit)", example="celsius")
    
class BatchConversionResponse(BaseModel):
    results: List[str] = Field(..., description="List of conversion results")
    total_converted: int = Field(..., description="Number of successful conversions")
    total_errors: int = Field(..., description="Number of failed conversions")

class HealthResponse(BaseModel):
    status: str = Field(..., description="Service status")
    soap_service_available: bool = Field(..., description="Whether SOAP service is available")
    version: str = Field(..., description="API version")

# API Routes

@app.get("/", response_model=dict)
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Temperature Conversion API",
        "description": "REST API wrapper for W3Schools SOAP Temperature Conversion Service",
        "version": "1.0.0",
        "endpoints": {
            "docs": "/docs",
            "health": "/health",
            "fahrenheit_to_celsius": "/convert/ftc",
            "celsius_to_fahrenheit": "/convert/ctf",
            "batch_conversion": "/convert/batch"
        }
    }

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    try:
        # Test SOAP service availability
        soap_available = False
        if soap_client:
            # Try a simple conversion to test connectivity
            test_result = soap_client.fahrenheit_to_celsius("32")
            soap_available = test_result is not None
    except Exception as e:
        logger.warning(f"SOAP service health check failed: {e}")
        soap_available = False
    
    return HealthResponse(
        status="healthy" if soap_available else "degraded",
        soap_service_available=soap_available,
        version="1.0.0"
    )

@app.post("/convert/ftc", response_model=TemperatureResponse)
async def fahrenheit_to_celsius(request: TemperatureRequest):
    """
    Convert Fahrenheit to Celsius
    
    - **temperature**: Temperature value in Fahrenheit (string)
    """
    if not soap_client:
        raise HTTPException(status_code=503, detail="SOAP service not available")
    
    try:
        converted = soap_client.fahrenheit_to_celsius(request.temperature)
        return TemperatureResponse(
            original=request.temperature,
            converted=converted,
            from_unit="fahrenheit",
            to_unit="celsius"
        )
    except Exception as e:
        logger.error(f"Error converting Fahrenheit to Celsius: {e}")
        raise HTTPException(status_code=500, detail=f"Conversion failed: {str(e)}")

@app.post("/convert/ctf", response_model=TemperatureResponse)
async def celsius_to_fahrenheit(request: TemperatureRequest):
    """
    Convert Celsius to Fahrenheit
    
    - **temperature**: Temperature value in Celsius (string)
    """
    if not soap_client:
        raise HTTPException(status_code=503, detail="SOAP service not available")
    
    try:
        converted = soap_client.celsius_to_fahrenheit(request.temperature)
        return TemperatureResponse(
            original=request.temperature,
            converted=converted,
            from_unit="celsius",
            to_unit="fahrenheit"
        )
    except Exception as e:
        logger.error(f"Error converting Celsius to Fahrenheit: {e}")
        raise HTTPException(status_code=500, detail=f"Conversion failed: {str(e)}")

@app.post("/convert/batch", response_model=BatchConversionResponse)
async def batch_conversion(request: BatchConversionRequest):
    """
    Convert multiple temperatures in batch
    
    - **temperatures**: List of temperature values
    - **from_unit**: Source unit (celsius or fahrenheit)
    """
    if not soap_client:
        raise HTTPException(status_code=503, detail="SOAP service not available")
    
    if not request.temperatures:
        raise HTTPException(status_code=400, detail="No temperatures provided")
    
    if request.from_unit.lower() not in ['celsius', 'fahrenheit']:
        raise HTTPException(status_code=400, detail="from_unit must be 'celsius' or 'fahrenheit'")
    
    try:
        results = soap_client.batch_conversion(request.temperatures, request.from_unit)
        
        # Count successful conversions vs errors
        successful = sum(1 for result in results if "=" in result)
        errors = len(results) - successful
        
        return BatchConversionResponse(
            results=results,
            total_converted=successful,
            total_errors=errors
        )
    except Exception as e:
        logger.error(f"Error in batch conversion: {e}")
        raise HTTPException(status_code=500, detail=f"Batch conversion failed: {str(e)}")

# Query parameter endpoints for simple GET requests
@app.get("/convert/ftc", response_model=TemperatureResponse)
async def fahrenheit_to_celsius_get(temperature: str = Query(..., description="Temperature in Fahrenheit")):
    """Convert Fahrenheit to Celsius using GET request"""
    request = TemperatureRequest(temperature=temperature)
    return await fahrenheit_to_celsius(request)

@app.get("/convert/ctf", response_model=TemperatureResponse)
async def celsius_to_fahrenheit_get(temperature: str = Query(..., description="Temperature in Celsius")):
    """Convert Celsius to Fahrenheit using GET request"""
    request = TemperatureRequest(temperature=temperature)
    return await celsius_to_fahrenheit(request)

# Error handlers
@app.exception_handler(404)
async def not_found_handler(request, exc):
    return {"error": "Endpoint not found", "message": "Please check the API documentation at /docs"}

@app.exception_handler(500)
async def internal_error_handler(request, exc):
    return {"error": "Internal server error", "message": "Please try again later"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
