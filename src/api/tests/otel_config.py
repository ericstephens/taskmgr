"""
OpenTelemetry configuration for the API tests.
"""
import os
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.sqlalchemy import SQLAlchemyInstrumentor

# OTLP endpoint - points to our collector container
OTLP_ENDPOINT = os.environ.get("OTLP_ENDPOINT", "localhost:4317")

def setup_tracer(service_name="taskmgr-api-tests"):
    """Set up the OpenTelemetry tracer."""
    # Create a resource with service name
    resource = Resource(attributes={
        SERVICE_NAME: service_name
    })
    
    # Create a tracer provider
    tracer_provider = TracerProvider(resource=resource)
    
    # Create an OTLP exporter with insecure option
    otlp_exporter = OTLPSpanExporter(
        endpoint=OTLP_ENDPOINT,
        insecure=True
    )
    
    # Add the exporter to the tracer provider
    tracer_provider.add_span_processor(BatchSpanProcessor(otlp_exporter))
    
    # Set the tracer provider
    trace.set_tracer_provider(tracer_provider)
    
    # Get a tracer
    tracer = trace.get_tracer(__name__)
    
    return tracer

def instrument_fastapi(app):
    """Instrument a FastAPI application."""
    FastAPIInstrumentor.instrument_app(app)

def instrument_sqlalchemy(engine):
    """Instrument SQLAlchemy."""
    SQLAlchemyInstrumentor().instrument(engine=engine)

def cleanup_tracer():
    """Clean up the tracer provider."""
    tracer_provider = trace.get_tracer_provider()
    if hasattr(tracer_provider, "shutdown"):
        tracer_provider.shutdown()
