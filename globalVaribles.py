queue = []
key = None
MAX_THREADS, THREADS = 10, []


# for sharing the window
shared_dict = {}
def set_global_var(key, value):
    shared_dict[key] = value