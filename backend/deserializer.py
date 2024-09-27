import pickle
import logging

def load_pickle(file_path, allow_dangerous_deserialization=True):
    if not allow_dangerous_deserialization:
        raise RuntimeError("Deserialization is disabled by default for security reasons. "
                           "Set 'allow_dangerous_deserialization=True' to enable.")
    
    try:
        with open(file_path, 'rb') as f:
            data = pickle.load(f)
        return data
    except Exception as e:
        logging.error(f"Failed to load pickle file: {file_path} with error: {e}")
        return None
