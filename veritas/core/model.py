"""
core/model.py — thin compatibility wrapper using AIModel
"""
try:
    from core.ai_model import AIModel as _AIModel
except Exception as _import_exc:
    _import_err_msg = str(_import_exc)
    class _AIModel:
        def __init__(self):
            self._unavailable_reason = _import_err_msg
        def generate(self, prompt):
            return "ERROR: core.ai_model not available: " + self._unavailable_reason

def load_model(model_path=None):
    return _AIModel()

def load_tokenizer(tokenizer_path=None):
    return "stub_tokenizer"

def load_memory(db_path=None):
    return {}

def save_memory(db_path, memory):
    pass

AIModel = _AIModel
