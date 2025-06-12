from flask import Flask, request, jsonify
from flask_cors import CORS

from agent import one_shot_agent

app = Flask(__name__)
CORS(app)

@app.route('/run_script', methods=['POST'])
def run_script():
    try:
        # Recupera i dati JSON dalla richiesta
        data = request.get_json()
        if not data or 'text_input' not in data:
            return jsonify({'error': 'Input non valido. Si attende un JSON con "text_input".'}), 400

        session_id = data['session_id']
        user_input = data['text_input']
        print(f"Input dell'utente: {user_input}")
        ai_result = one_shot_agent(user_input, session_id)
        print(f"Output dell'AI: {ai_result}")
        return jsonify({'result': ai_result})

    except Exception as e:
        # Gestione degli errori generici
        print(f"Errore durante l'elaborazione della richiesta: {e}")
        return jsonify({'error': 'Errore interno del server.'}), 500

@app.route('/')
def index():
    # Restituisce una semplice pagina HTML per testare l'API.
    return '''
    <html>
        <head><title>Test API</title></head>
        <body>
            <h1>API di Test</h1>
            <p>Invia una richiesta POST a /run_script con un JSON contenente "text_input".</p>
        </body>
    </html>
    '''


if __name__ == '__main__':
    # Esegui l'applicazione Flask in modalità debug.
    # In produzione, usa un server WSGI come Gunicorn o uWSGI.
    app.run(debug=True)
