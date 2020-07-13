from src.app import app
from src.config import PORT
import conversation
import sentimentAnalys
import recomendation

app.run("0.0.0.0", PORT, debug=True)