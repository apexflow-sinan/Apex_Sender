"""Web server for Apex Sender"""
import os
import sys
import socket
from flask import Flask, render_template, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename

# Get base path (works with PyInstaller)
def get_base_path():
    if getattr(sys, 'frozen', False):
        # Running as compiled executable
        if hasattr(sys, '_MEIPASS'):
            # PyInstaller temp folder
            return sys._MEIPASS
        else:
            # Fallback to executable directory
            return os.path.dirname(sys.executable)
    else:
        # Running as script
        return os.path.dirname(os.path.dirname(__file__))

# Add project root to path
project_root = get_base_path()
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from src.config.settings import DEFAULT_PORT, BUFFER_SIZE

# Create Flask app with correct paths
base_path = get_base_path()
template_folder = os.path.join(base_path, 'web', 'templates')
static_folder = os.path.join(base_path, 'web', 'static')

app = Flask(__name__, template_folder=template_folder, static_folder=static_folder)
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024 * 1024  # 10GB max

# Use user directory for temp uploads (not inside exe)
UPLOAD_FOLDER = os.path.join(os.path.expanduser('~'), 'AppData', 'Local', 'ApexSender', 'temp_uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.after_request
def add_pwa_headers(response):
    """Add PWA headers"""
    # PWA headers
    if request.path == '/static/manifest.json':
        response.headers['Content-Type'] = 'application/manifest+json'
    if request.path == '/static/service-worker.js':
        response.headers['Content-Type'] = 'application/javascript'
        response.headers['Service-Worker-Allowed'] = '/'
    
    # Disable caching for JS/CSS files during development
    if request.path.endswith(('.js', '.css')):
        response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '0'
    
    # Security headers
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    
    return response

@app.route('/')
def index():
    """Default route"""
    from src.utils.network_utils import get_local_ip
    ip = get_local_ip()
    parts = ip.split('.')
    return render_template('index_bottom_nav.html', ip_parts=parts, full_ip=ip, port=DEFAULT_PORT)

@app.route('/bottom-nav')
def bottom_nav():
    """Bottom navigation version (mobile-first)"""
    from src.utils.network_utils import get_local_ip
    ip = get_local_ip()
    parts = ip.split('.')
    return render_template('index_bottom_nav.html', ip_parts=parts, full_ip=ip, port=DEFAULT_PORT)

@app.route('/sidebar')
def sidebar():
    """Sidebar navigation version"""
    from src.utils.network_utils import get_local_ip
    ip = get_local_ip()
    parts = ip.split('.')
    return render_template('index_bottom_nav.html', ip_parts=parts, full_ip=ip, port=DEFAULT_PORT)

@app.route('/classic')
def classic():
    """Classic version"""
    from src.utils.network_utils import get_local_ip
    ip = get_local_ip()
    parts = ip.split('.')
    return render_template('index_bottom_nav.html', ip_parts=parts, full_ip=ip, port=DEFAULT_PORT)

@app.route('/api/network-info')
def network_info():
    """Get network information"""
    from src.utils.network_utils import get_local_ip
    return jsonify({
        'server_ip': get_local_ip(),
        'port': DEFAULT_PORT
    })

@app.route('/api/received-files')
def received_files():
    """Get list of received files (sorted by newest first)"""
    from src.core.settings_manager import SettingsManager
    settings = SettingsManager()
    save_dir = settings.get('save_directory')
    
    try:
        files = []
        if os.path.exists(save_dir):
            for filename in os.listdir(save_dir):
                # Skip hidden files and system files
                if filename.startswith('.') or filename in ['Thumbs.db', 'desktop.ini']:
                    continue
                    
                filepath = os.path.join(save_dir, filename)
                if os.path.isfile(filepath):
                    size = os.path.getsize(filepath)
                    mtime = os.path.getmtime(filepath)
                    files.append({
                        'name': filename,
                        'size': size,
                        'size_mb': round(size / 1024 / 1024, 2),
                        'mtime': mtime
                    })
            # Sort by modification time (newest first)
            files.sort(key=lambda x: x['mtime'], reverse=True)
        return jsonify({'files': files})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/delete-file/<filename>', methods=['POST'])
def delete_file(filename):
    """Delete a file from server"""
    from src.core.settings_manager import SettingsManager
    settings = SettingsManager()
    save_dir = settings.get('save_directory')
    filepath = os.path.join(save_dir, filename)
    
    try:
        if os.path.exists(filepath):
            os.remove(filepath)
            return jsonify({'status': 'success'})
        return jsonify({'status': 'error', 'message': 'File not found'}), 404
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/delete-all-files', methods=['POST'])
def delete_all_files():
    """Delete all files from server"""
    from src.core.settings_manager import SettingsManager
    settings = SettingsManager()
    save_dir = settings.get('save_directory')
    
    try:
        deleted = 0
        if os.path.exists(save_dir):
            for filename in os.listdir(save_dir):
                # Skip hidden files and system files
                if filename.startswith('.') or filename in ['Thumbs.db', 'desktop.ini']:
                    continue
                    
                filepath = os.path.join(save_dir, filename)
                if os.path.isfile(filepath):
                    os.remove(filepath)
                    deleted += 1
        return jsonify({'status': 'success', 'deleted': deleted})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/download/<filename>')
def download_file(filename):
    """Download a received file and delete from server"""
    from src.core.settings_manager import SettingsManager
    from flask import Response
    settings = SettingsManager()
    save_dir = settings.get('save_directory')
    filepath = os.path.join(save_dir, filename)
    
    if not os.path.exists(filepath):
        return jsonify({'status': 'error', 'message': 'File not found'}), 404
    
    # Read file and delete immediately
    try:
        with open(filepath, 'rb') as f:
            file_data = f.read()
        os.remove(filepath)
        
        return Response(
            file_data,
            mimetype='application/octet-stream',
            headers={'Content-Disposition': f'attachment; filename="{filename}"'}
        )
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/shutdown', methods=['POST'])
def shutdown():
    """Shutdown the server"""
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        # For production servers, just return success
        return jsonify({'status': 'success'})
    func()
    return jsonify({'status': 'success', 'message': 'Server shutting down...'})

@app.route('/send', methods=['POST'])
def send_file():
    filepath = None
    try:
        if 'file' not in request.files:
            return jsonify({'status': 'error', 'message': 'لم يتم اختيار ملف'}), 400
        
        file = request.files['file']
        ip = request.form['ip']
        port = int(request.form.get('port', DEFAULT_PORT))
        
        # Get original filename
        original_filename = file.filename
        filename = secure_filename(original_filename)
        if not filename:
            filename = original_filename
        
        # Save temporarily for reliable transfer
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)
        file_size = os.path.getsize(filepath)
        
        _send_via_socket(ip, port, original_filename, filepath, file_size)
        
        os.remove(filepath)
        return jsonify({'status': 'success', 'message': 'تم الإرسال بنجاح'})
    except Exception as e:
        if filepath and os.path.exists(filepath):
            try:
                os.remove(filepath)
            except:
                pass
        import traceback
        print(f"Error sending file: {traceback.format_exc()}")
        return jsonify({'status': 'error', 'message': f'خطأ: {str(e)}'}), 500


@app.route('/send-text', methods=['POST'])
def send_text():
    """Send text message to a device"""
    filepath = None
    try:
        data = request.get_json()
        text = data.get('text', '').strip()
        ip = data.get('ip', '').strip()
        port = int(data.get('port', DEFAULT_PORT))
        
        if not text:
            return jsonify({'status': 'error', 'message': 'النص فارغ'}), 400
        if not ip:
            return jsonify({'status': 'error', 'message': 'عنوان IP مطلوب'}), 400
        
        filepath = os.path.join(UPLOAD_FOLDER, '__APEX_TEXT__')
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(text)
        file_size = os.path.getsize(filepath)
        
        _send_via_socket(ip, port, '__APEX_TEXT__', filepath, file_size)
        
        os.remove(filepath)
        return jsonify({'status': 'success', 'message': 'تم إرسال النص بنجاح'})
    except Exception as e:
        if filepath and os.path.exists(filepath):
            try:
                os.remove(filepath)
            except:
                pass
        return jsonify({'status': 'error', 'message': f'خطأ: {str(e)}'}), 500


def _send_via_socket(ip, port, filename, filepath, file_size):
    """Send file via TCP socket"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(60)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 2 * 1024 * 1024)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 2 * 1024 * 1024)
        s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        s.connect((ip, port))
        s.sendall(f"{filename}\n{file_size}\n".encode('utf-8'))
        
        chunk_size = 256 * 1024
        with open(filepath, 'rb') as f:
            sent = 0
            while sent < file_size:
                chunk = f.read(chunk_size)
                if not chunk:
                    break
                s.sendall(chunk)
                sent += len(chunk)

def start_server(port=8080, use_ssl=False):
    """Start the web server"""
    # Optimize Flask for better performance
    from werkzeug.serving import WSGIRequestHandler
    WSGIRequestHandler.protocol_version = "HTTP/1.1"
    
    if use_ssl:
        # Try to use SSL if certificates exist
        cert_file = 'cert.pem'
        key_file = 'key.pem'
        if os.path.exists(cert_file) and os.path.exists(key_file):
            context = (cert_file, key_file)
            print(f"Starting HTTPS server on port {port}")
            app.run(host='0.0.0.0', port=port, debug=False, threaded=True, 
                   ssl_context=context, request_handler=WSGIRequestHandler)
        else:
            print(f"SSL certificates not found, starting HTTP server on port {port}")
            app.run(host='0.0.0.0', port=port, debug=False, threaded=True,
                   request_handler=WSGIRequestHandler)
    else:
        print(f"Starting HTTP server on port {port}")
        app.run(host='0.0.0.0', port=port, debug=False, threaded=True,
               request_handler=WSGIRequestHandler)
