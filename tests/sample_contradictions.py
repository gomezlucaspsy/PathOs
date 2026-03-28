# test_sample.py — intentional circular + dead code for demonstration

# Simulates a circular call chain: a -> b -> c -> a
def process_data(data):
    return validate(data)

def validate(data):
    return transform(data)

def transform(data):
    return process_data(data)  # loops back — circular

# Dead code: defined but never called or referenced
def orphaned_utility():
    pass

class ForgottenService:
    def run(self):
        orphaned_utility()
