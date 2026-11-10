import unittest
from tasks import agregar_tarea, completar_tarea, eliminar_tarea, pendientes

class TestTasks(unittest.TestCase):
    def test_agregar_tarea(self):
        tareas = []
        tarea = agregar_tarea(tareas, "Leer documentación", "estudio")
        self.assertEqual(tarea["titulo"], "Leer documentación")
        self.assertEqual(tarea["categoria"], "estudio")
        self.assertFalse(tarea["completada"])

    def test_completar_tarea(self):
        tareas = []
        agregar_tarea(tareas, "Practicar", "práctica")
        completar_tarea(tareas, 1)
        self.assertEqual(pendientes(tareas), [])

    def test_agregar_tarea_categoria_vacia(self):
        tareas = []
        with self.assertRaises(ValueError):
            agregar_tarea(tareas, "Leer documentación", "   ")

    def test_pendientes_filtra_por_categoria_sin_mayusculas(self):
        tareas = []
        agregar_tarea(tareas, "Leer documentación", "Estudio")
        agregar_tarea(tareas, "Comprar cuaderno", "Compras")
        filtradas = pendientes(tareas, "eStUdIo")
        self.assertEqual(len(filtradas), 1)
        self.assertEqual(filtradas[0]["titulo"], "Leer documentación")

    def test_pendientes_categoria_inexistente_devuelve_vacia(self):
        tareas = []
        agregar_tarea(tareas, "Leer documentación", "Estudio")
        agregar_tarea(tareas, "Comprar cuaderno", "Compras")
        self.assertEqual(pendientes(tareas, "Salud"), [])

    def test_eliminar_tarea_existente_devuelve_tarea_eliminada(self):
        tareas = []
        agregar_tarea(tareas, "Leer documentación", "Estudio")
        agregar_tarea(tareas, "Comprar cuaderno", "Compras")
        eliminada = eliminar_tarea(tareas, 1)
        self.assertEqual(eliminada["id"], 1)
        self.assertEqual(len(tareas), 1)
        self.assertEqual(tareas[0]["id"], 2)

    def test_eliminar_tarea_id_inexistente_lanza_value_error(self):
        tareas = []
        agregar_tarea(tareas, "Leer documentación", "Estudio")
        with self.assertRaisesRegex(ValueError, "Tarea no encontrada"):
            eliminar_tarea(tareas, 99)

    def test_eliminar_tarea_no_reindexa_ids_restantes(self):
        tareas = []
        agregar_tarea(tareas, "Tarea 1", "General")
        agregar_tarea(tareas, "Tarea 2", "General")
        agregar_tarea(tareas, "Tarea 3", "General")
        eliminar_tarea(tareas, 2)
        self.assertEqual([t["id"] for t in tareas], [1, 3])

    def test_agregar_tarea_no_repite_id_despues_de_eliminar(self):
        tareas = []
        agregar_tarea(tareas, "Tarea 1", "General")
        agregar_tarea(tareas, "Tarea 2", "General")
        agregar_tarea(tareas, "Tarea 3", "General")
        eliminar_tarea(tareas, 2)
        nueva = agregar_tarea(tareas, "Tarea nueva", "General")
        self.assertEqual(nueva["id"], 4)
        self.assertEqual(sorted(t["id"] for t in tareas), [1, 3, 4])

if __name__ == "__main__":
    unittest.main()
