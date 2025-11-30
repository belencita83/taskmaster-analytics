# debug_gestor.py
from core.storage import GestorAlmacenamiento

gestor = GestorAlmacenamiento("sqlite")
print("Atributos de GestorAlmacenamiento:")
print(f"  Tipo: {type(gestor)}")
print(f"  Dir: {[attr for attr in dir(gestor) if not attr.startswith('_')]}")
print(f"  Dict: {gestor.__dict__}")