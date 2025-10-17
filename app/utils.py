# app/utils.py
def language_from_filename(filename: str) -> str:
    fn = filename.lower()
    if fn.endswith('.py'):
        return 'python'
    if fn.endswith('.js') or fn.endswith('.ts'):
        return 'javascript/typescript'
    if fn.endswith('.java'):
        return 'java'
    if fn.endswith('.cpp') or fn.endswith('.cc') or fn.endswith('.c'):
        return 'c/c++'
    if fn.endswith('.go'):
        return 'go'
    if fn.endswith('.rs'):
        return 'rust'
    if fn.endswith('.rb'):
        return 'ruby'
    return 'unknown'