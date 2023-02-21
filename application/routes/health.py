from flask import current_app

@current_app.route('/health', methods=['GET'])
def health():
    return 'OK'
