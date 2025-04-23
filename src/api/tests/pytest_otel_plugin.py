"""
Pytest plugin for OpenTelemetry integration.
"""
import pytest
from opentelemetry import trace
from opentelemetry.trace.status import Status, StatusCode

@pytest.hookimpl(tryfirst=True)
def pytest_runtest_setup(item):
    """Set up a span for each test."""
    # Get the tracer
    tracer = trace.get_tracer("pytest-plugin")
    
    # Start a span for the test
    span = tracer.start_span(f"test_setup:{item.nodeid}")
    
    # Store the span in the item for later use
    item._otel_span = span

@pytest.hookimpl(trylast=True)
def pytest_runtest_teardown(item):
    """Tear down the span for each test."""
    if hasattr(item, "_otel_span"):
        # End the span
        item._otel_span.end()

@pytest.hookimpl(tryfirst=True)
def pytest_runtest_call(item):
    """Set up a span for the test execution."""
    # Get the tracer
    tracer = trace.get_tracer("pytest-plugin")
    
    # Start a span for the test execution
    span = tracer.start_span(f"test_execution:{item.nodeid}")
    
    # Store the span in the item for later use
    item._otel_execution_span = span

@pytest.hookimpl(trylast=True)
def pytest_runtest_makereport(item, call):
    """Create a report for the test execution."""
    if call.when == "call" and hasattr(item, "_otel_execution_span"):
        span = item._otel_execution_span
        
        # Add test result to the span
        if call.excinfo is None:
            span.set_status(Status(StatusCode.OK))
            span.set_attribute("test.result", "passed")
        else:
            span.set_status(Status(StatusCode.ERROR))
            span.set_attribute("test.result", "failed")
            span.set_attribute("test.error", str(call.excinfo.value))
            span.set_attribute("test.traceback", str(call.excinfo.traceback))
        
        # End the span
        span.end()

@pytest.hookimpl(trylast=True)
def pytest_sessionfinish(session, exitstatus):
    """Clean up the tracer at the end of the test session."""
    # Import the cleanup function
    from api.tests.otel_config import cleanup_tracer
    
    # Clean up the tracer
    cleanup_tracer()
