import pype

@pype.component
def external_function(x):
    return x + 5

def not_decorated_function(x):
    return x + 5