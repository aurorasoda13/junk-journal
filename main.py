import psycopg2
from flask import Flask, render_template, request, redirect, send_file, url_for
from datetime import timedelta
from io import BytesIO

# Connessione al database Neon
connection = psycopg2.connect(
    host="ep-wispy-cake-amf1vlc6-pooler.c-5.us-east-1.aws.neon.tech",
    port=5432,
    database="neondb",
    user="neondb_owner",
    password="npg_hmsc9tN2SXrB",
    sslmode="require"
)

app = Flask(__name__)
app.secret_key = "una-chiave-super-segreta"
app.permanent_session_lifetime = timedelta(minutes=30)


# ---------------------------
# PAGINA INIZIALE
# ---------------------------
@app.route("/")
def index():
    return render_template("diari.html")


# ---------------------------
# DIARIO UTENTE
# ---------------------------
@app.route("/diario/<utente>")
def diario(utente):
    cursor = connection.cursor()

    # Recupera ID utente
    cursor.execute("SELECT id FROM utente WHERE nome = %s", (utente,))
    user_row = cursor.fetchone()

    if not user_row:
        return "Utente non trovato", 404

    utenteid = user_row[0]

    # Recupera immagini dell'utente
    cursor.execute("""
        SELECT id, filename 
        FROM images 
        WHERE utente = %s
        ORDER BY id ASC
    """, (utenteid,))
    immagini = cursor.fetchall()
    cursor.close()

  # Tutte le immagini sono pagine singole
    pagine = immagini


    return render_template("diario.html", utente=utente, pagine=pagine)

@app.route("/diario/<utente>/didascalia/<image_id>", methods=["POST"])
def update_caption(utente, image_id):
    caption = request.form.get("didascalia", "")

    cursor = connection.cursor()
    cursor.execute(
        "UPDATE images SET didascalia = %s WHERE id = %s",
        (caption, image_id)
    )
    connection.commit()
    cursor.close()

    return "OK"

# ---------------------------
# UPLOAD DI UNA PAGINA NEL DIARIO
# ---------------------------
@app.route("/diario/<utente>/upload", methods=["POST"])
def upload_diario(utente):
    cursor = connection.cursor()

    # Recupera ID utente
    cursor.execute("SELECT id FROM utente WHERE nome = %s", (utente,))
    user_row = cursor.fetchone()

    if not user_row:
        return "Utente non trovato", 404

    user_id = user_row[0]

    # File caricato
    file = request.files["image"]
    filename = file.filename
    binary_data = file.read()

    # Salva nel DB
    cursor.execute(
        "INSERT INTO images (filename, data, utente) VALUES (%s, %s, %s)",
        (filename, psycopg2.Binary(binary_data), user_id)
    )
    connection.commit()
    cursor.close()

    return redirect(url_for("diario", utente=utente))


# ---------------------------
# MOSTRA IMMAGINE
# ---------------------------
@app.route("/image/<int:image_id>")
def get_image(image_id):
    cursor = connection.cursor()
    cursor.execute("SELECT filename, data FROM images WHERE id = %s", (image_id,))
    row = cursor.fetchone()
    cursor.close()

    if not row:
        return "Immagine non trovata", 404

    filename, binary_data = row

    return send_file(BytesIO(binary_data), mimetype="image/jpeg", download_name=filename)

@app.route("/delete/<int:image_id>", methods=["POST"])
def delete_page(image_id):
    cursor = connection.cursor()
    cursor.execute("DELETE FROM images WHERE id = %s", (image_id,))
    connection.commit()
    cursor.close()

    # Torna alla pagina precedente
    referer = request.headers.get("Referer")
    return redirect(referer or url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
