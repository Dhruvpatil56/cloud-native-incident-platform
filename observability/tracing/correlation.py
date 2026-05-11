from opentelemetry.trace import get_current_span


def get_trace_id():

    span = get_current_span()

    trace_id = format(span.get_span_context().trace_id, '032x')

    return trace_id
