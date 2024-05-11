import sys
import json
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QComboBox, \
    QLineEdit, QTextEdit, QFileDialog, QMessageBox, QGraphicsView, QGraphicsScene, QInputDialog
from PyQt5.QtGui import QColor, QBrush, QPen
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QGraphicsEllipseItem, QGraphicsRectItem, QGraphicsTextItem, QGraphicsLineItem


class Node:
    def __init__(self, data):
        self.data = data
        self.left = None
        self.right = None


class Stack:
    def __init__(self):
        self.top = None

    def push(self, data):
        new_node = Node(data)
        new_node.next = self.top
        self.top = new_node

    def pop(self):
        if self.top:
            removed = self.top.data
            self.top = self.top.next
            return removed
        return None

    def peek(self):
        return self.top.data if self.top else None


class Queue:
    def __init__(self):
        self.front = None
        self.rear = None

    def enqueue(self, data):
        new_node = Node(data)
        if not self.front:
            self.front = new_node
            self.rear = new_node
        else:
            self.rear.next = new_node
            self.rear = new_node

    def dequeue(self):
        if self.front:
            removed = self.front.data
            self.front = self.front.next
            return removed
        return None

    def peek(self):
        return self.front.data if self.front else None


class Node:
    def __init__(self, data):
        self.data = data
        self.next = None


class LinkedList:
    def __init__(self):
        self.head = None

    def insert_end(self, data):
        if not self.head:
            self.head = Node(data)
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = Node(data)

    def search(self, data):
        current = self.head
        while current:
            if current.data == data:
                return True
            current = current.next
        return False


class CircularLinkedList(LinkedList):
    def insert_end(self, data):
        if not self.head:
            self.head = Node(data)
            self.head.next = self.head
        else:
            current = self.head
            while current.next != self.head:
                current = current.next
            current.next = Node(data)
            current.next.next = self.head


class DoublyLinkedList(Node):
    def __init__(self):
        super().__init__(None)
        self.head = None

    def insert_end(self, data):
        if not self.head:
            self.head = Node(data)
        else:
            current = self.head
            while current.next:
                current = current.next
            new_node = Node(data)
            current.next = new_node
            new_node.prev = current

    def search(self, data):
        current = self.head
        while current:
            if current.data == data:
                return True
            current = current.next
        return False


class CircularDoublyLinkedList(DoublyLinkedList):
    def insert_end(self, data):
        if not self.head:
            self.head = Node(data)
            self.head.next = self.head
            self.head.prev = self.head
        else:
            current = self.head
            while current.next != self.head:
                current = current.next
            new_node = Node(data)
            current.next = new_node
            new_node.prev = current
            new_node.next = self.head
            self.head.prev = new_node


class BinaryTree:
    def __init__(self, data):
        self.data = data
        self.left = None
        self.right = None

    def insert(self, data):
        if self.data:
            if data < self.data:
                if self.left is None:
                    self.left = BinaryTree(data)
                else:
                    self.left.insert(data)
            elif data > self.data:
                if self.right is None:
                    self.right = BinaryTree(data)
                else:
                    self.right.insert(data)
        else:
            self.data = data

    def search(self, data):
        if data < self.data:
            if self.left is None:
                return False
            return self.left.search(data)
        elif data > self.data:
            if self.right is None:
                return False
            return self.right.search(data)
        else:
            return True

    def delete(self, data):
        if data < self.data:
            if self.left:
                self.left = self.left.delete(data)
        elif data > self.data:
            if self.right:
                self.right = self.right.delete(data)
        else:
            if self.left is None and self.right is None:
                return None
            elif self.left is None:
                return self.right
            elif self.right is None:
                return self.left
            min_value = self.right.find_min()
            self.data = min_value
            self.right = self.right.delete(min_value)
        return self

    def find_min(self):
        if self.left:
            return self.left.find_min()
        return self.data

    def height(self):
        if not self:
            return 0
        left_height = self.left.height() if self.left else 0
        right_height = self.right.height() if self.right else 0
        return max(left_height, right_height) + 1


class BinarySearchTree(BinaryTree):
    def __init__(self, data):
        super().__init__(data)

    def insert(self, data):
        if data < self.data:
            if self.left is None:
                self.left = BinarySearchTree(data)
            else:
                self.left.insert(data)
        elif data > self.data:
            if self.right is None:
                self.right = BinarySearchTree(data)
            else:
                self.right.insert(data)


class DataStructureApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Software Educativo - Estructuras de Datos")
        self.setGeometry(100, 100, 800, 600)

        self.layout = QVBoxLayout()

        # Selector de estructura de datos y tipo de dato
        self.structure_label = QLabel("Estructura de datos:")
        self.structure_combo = QComboBox()
        self.structure_combo.addItems(["Pila", "Cola", "Lista simplemente enlazada", "Lista circular",
                                        "Lista doblemente enlazada", "Lista circular doble", "Árbol binario",
                                        "Árbol de búsqueda"])
        self.data_type_label = QLabel("Tipo de dato:")
        self.data_type_combo = QComboBox()
        self.data_types = ["Números enteros", "Números flotantes", "Valores lógicos", "Cadenas de texto"]
        self.data_type_combo.addItems(self.data_types)

        # Botones de acción
        self.actions_label = QLabel("Acciones:")
        self.action_buttons_layout = QHBoxLayout()
        self.insert_button = QPushButton("Insertar dato")
        self.delete_button = QPushButton("Eliminar dato")
        self.search_button = QPushButton("Buscar dato")
        self.save_button = QPushButton("Guardar estructura de datos")
        self.load_button = QPushButton("Cargar estructura de datos")
        self.new_structure_button = QPushButton("Nueva estructura")
        self.action_buttons_layout.addWidget(self.insert_button)
        self.action_buttons_layout.addWidget(self.delete_button)
        self.action_buttons_layout.addWidget(self.search_button)
        self.action_buttons_layout.addWidget(self.save_button)
        self.action_buttons_layout.addWidget(self.load_button)
        self.action_buttons_layout.addWidget(self.new_structure_button)
        self.layout.addWidget(self.structure_label)
        self.layout.addWidget(self.structure_combo)
        self.layout.addWidget(self.data_type_label)
        self.layout.addWidget(self.data_type_combo)
        self.layout.addWidget(self.actions_label)
        self.layout.addLayout(self.action_buttons_layout)

        # Vista de la estructura de datos
        self.data_structure_view = QGraphicsView()
        self.scene = QGraphicsScene()
        self.data_structure_view.setScene(self.scene)
        self.layout.addWidget(self.data_structure_view)

        # Conectar señales y slots
        self.insert_button.clicked.connect(self.insert_data)
        self.delete_button.clicked.connect(self.delete_data)
        self.search_button.clicked.connect(self.search_data)
        self.save_button.clicked.connect(self.save_data)
        self.load_button.clicked.connect(self.load_data)
        self.new_structure_button.clicked.connect(self.new_structure)

        # Estructura de datos actual
        self.data_structure = None

        self.setLayout(self.layout)

    def new_structure(self):
        self.data_structure = None
        self.update_data_structure_view()

    def insert_data(self):
        data_type = self.data_type_combo.currentText()
        if data_type == 'Números enteros':
            data_text, ok = QInputDialog.getText(self, "Insertar dato", "Ingrese el número entero:")
            if ok:
                data = int(data_text)
            else:
                return
        elif data_type == 'Números flotantes':
            data_text, ok = QInputDialog.getText(self, "Insertar dato", "Ingrese el número flotante:")
            if ok:
                data = float(data_text)
            else:
                return
        elif data_type == 'Valores lógicos':
            data_text, ok = QInputDialog.getText(self, "Insertar dato", "Ingrese el valor lógico (True o False):")
            if ok:
                data = True if data_text.lower() == 'true' else False
            else:
                return
        elif data_type == 'Cadenas de texto':
            data_text, ok = QInputDialog.getText(self, "Insertar dato", "Ingrese la cadena de texto:")
            if ok:
                data = str(data_text)
            else:
                return
        else:
            return

        structure = self.structure_combo.currentText()
        if structure == 'Pila':
            if not self.data_structure:
                self.data_structure = Stack()
            self.data_structure.push(data)
        elif structure == 'Cola':
            if not self.data_structure:
                self.data_structure = Queue()
            self.data_structure.enqueue(data)
        elif structure == 'Lista simplemente enlazada':
            if not self.data_structure:
                self.data_structure = LinkedList()
            self.data_structure.insert_end(data)
        elif structure == 'Lista circular':
            if not self.data_structure:
                self.data_structure = CircularLinkedList()
            self.data_structure.insert_end(data)
        elif structure == 'Lista doblemente enlazada':
            if not self.data_structure:
                self.data_structure = DoublyLinkedList()
            self.data_structure.insert_end(data)
        elif structure == 'Lista circular doble':
            if not self.data_structure:
                self.data_structure = CircularDoublyLinkedList()
            self.data_structure.insert_end(data)
        elif structure == 'Árbol binario':
            if not self.data_structure:
                data_text, ok = QInputDialog.getText(self, "Insertar dato", "Ingrese el número entero para la raíz del árbol:")
                if ok:
                    data = int(data_text)
                    self.data_structure = BinaryTree(data)
                else:
                    return
            else:
                self.data_structure.insert(data)
        elif structure == 'Árbol de búsqueda':
            if not self.data_structure:
                data_text, ok = QInputDialog.getText(self, "Insertar dato", "Ingrese el número entero para la raíz del árbol:")
                if ok:
                    data = int(data_text)
                    self.data_structure = BinarySearchTree(data)
                else:
                    return
            else:
                self.data_structure.insert(data)

        self.update_data_structure_view()

    def delete_data(self):
        if not self.data_structure:
            return

        data_type = self.data_type_combo.currentText()
        if data_type == 'Números enteros':
            data_text, ok = QInputDialog.getText(self, "Eliminar dato", "Ingrese el número entero a eliminar:")
            if ok:
                data = int(data_text)
            else:
                return
        elif data_type == 'Números flotantes':
            data_text, ok = QInputDialog.getText(self, "Eliminar dato", "Ingrese el número flotante a eliminar:")
            if ok:
                data = float(data_text)
            else:
                return
        elif data_type == 'Valores lógicos':
            data_text, ok = QInputDialog.getText(self, "Eliminar dato", "Ingrese el valor lógico a eliminar (True o False):")
            if ok:
                data = True if data_text.lower() == 'true' else False
            else:
                return
        elif data_type == 'Cadenas de texto':
            data_text, ok = QInputDialog.getText(self, "Eliminar dato", "Ingrese la cadena de texto a eliminar:")
            if ok:
                data = str(data_text)
            else:
                return
        else:
            return

        structure = self.structure_combo.currentText()
        if structure == 'Pila':
            if not self.data_structure:
                return
            if self.data_structure.peek() == data:
                self.data_structure.pop()
        elif structure == 'Cola':
            if not self.data_structure:
                return
            if self.data_structure.peek() == data:
                self.data_structure.dequeue()
        elif structure == 'Lista simplemente enlazada':
            if not self.data_structure:
                return
            if self.data_structure.head.data == data:
                self.data_structure.head = self.data_structure.head.next
        elif structure == 'Lista circular':
            if not self.data_structure:
                return
            if self.data_structure.head.data == data:
                current = self.data_structure.head
                while current.next != self.data_structure.head:
                    current = current.next
                current.next = self.data_structure.head.next
                self.data_structure.head = self.data_structure.head.next
        elif structure == 'Lista doblemente enlazada':
            if not self.data_structure:
                return
            if self.data_structure.head.data == data:
                self.data_structure.head = self.data_structure.head.next
                if self.data_structure.head:
                    self.data_structure.head.prev = None
        elif structure == 'Lista circular doble':
            if not self.data_structure:
                return
            if self.data_structure.head.data == data:
                current = self.data_structure.head
                while current.next != self.data_structure.head:
                    current = current.next
                current.next = self.data_structure.head.next
                self.data_structure.head = self.data_structure.head.next
                if self.data_structure.head:
                    self.data_structure.head.prev = current
        elif structure == 'Árbol binario' or structure == 'Árbol de búsqueda':
            if not self.data_structure:
                return
            self.data_structure = self.data_structure.delete(data)

        self.update_data_structure_view()

    def search_data(self):
        if not self.data_structure:
            return

        data_type = self.data_type_combo.currentText()
        if data_type == 'Números enteros':
            data_text, ok = QInputDialog.getText(self, "Buscar dato", "Ingrese el número entero a buscar:")
            if ok:
                data = int(data_text)
            else:
                return
        elif data_type == 'Números flotantes':
            data_text, ok = QInputDialog.getText(self, "Buscar dato", "Ingrese el número flotante a buscar:")
            if ok:
                data = float(data_text)
            else:
                return
        elif data_type == 'Valores lógicos':
            data_text, ok = QInputDialog.getText(self, "Buscar dato", "Ingrese el valor lógico a buscar (True o False):")
            if ok:
                data = True if data_text.lower() == 'true' else False
            else:
                return
        elif data_type == 'Cadenas de texto':
            data_text, ok = QInputDialog.getText(self, "Buscar dato", "Ingrese la cadena de texto a buscar:")
            if ok:
                data = str(data_text)
            else:
                return
        else:
            return

        structure = self.structure_combo.currentText()
        found = False
        if structure == 'Pila':
            found = self.data_structure.search(data)
        elif structure == 'Cola':
            found = self.data_structure.search(data)
        elif structure == 'Lista simplemente enlazada':
            found = self.data_structure.search(data)
        elif structure == 'Lista circular':
            found = self.data_structure.search(data)
        elif structure == 'Lista doblemente enlazada':
            found = self.data_structure.search(data)
        elif structure == 'Lista circular doble':
            found = self.data_structure.search(data)
        elif structure == 'Árbol binario' or structure == 'Árbol de búsqueda':
            found = self.data_structure.search(data)

        if found:
            QMessageBox.information(self, "Búsqueda exitosa", f"El dato {data} se encuentra en la estructura de datos.")
        else:
            QMessageBox.information(self, "Búsqueda fallida", f"El dato {data} no se encuentra en la estructura de datos.")

    def save_data(self):
        if not self.data_structure:
            QMessageBox.warning(self, "Guardar estructura de datos", "No hay una estructura de datos para guardar.")
            return

        filename, _ = QFileDialog.getSaveFileName(self, "Guardar estructura de datos", "", "Archivos JSON (*.json)")
        if filename:
            data = {
                "structure": self.structure_combo.currentText(),
                "type": self.data_type_combo.currentText()
            }
            if isinstance(self.data_structure, Stack) or isinstance(self.data_structure, Queue):
                items = []
                item = self.data_structure.pop() if isinstance(self.data_structure, Stack) else self.data_structure.dequeue()
                while item:
                    items.append(item)
                    item = self.data_structure.pop() if isinstance(self.data_structure, Stack) else self.data_structure.dequeue()
                data["items"] = items
            elif isinstance(self.data_structure, (LinkedList, CircularLinkedList, DoublyLinkedList, CircularDoublyLinkedList)):
                items = []
                current = self.data_structure.head
                while current:
                    items.append(current.data)
                    current = current.next
                data["items"] = items
            elif isinstance(self.data_structure, (BinaryTree, BinarySearchTree)):
                def traverse(node):
                    if not node:
                        return []
                    return [node.data] + traverse(node.left) + traverse(node.right)
                data["items"] = traverse(self.data_structure)

            with open(filename, 'w') as f:
                json.dump(data, f, indent=4)

    def load_data(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Cargar estructura de datos", "", "Archivos JSON (*.json)")
        if filename:
            with open(filename, 'r') as f:
                data = json.load(f)
            structure = data["structure"]
            data_type = data["type"]
            items = data.get("items", [])
            if structure == "Pila":
                self.data_structure = Stack()
            elif structure == "Cola":
                self.data_structure = Queue()
            elif structure == "Lista simplemente enlazada":
                self.data_structure = LinkedList()
            elif structure == "Lista circular":
                self.data_structure = CircularLinkedList()
            elif structure == "Lista doblemente enlazada":
                self.data_structure = DoublyLinkedList()
            elif structure == "Lista circular doble":
                self.data_structure = CircularDoublyLinkedList()
            elif structure == "Árbol binario":
                self.data_structure = BinaryTree(None)
            elif structure == "Árbol de búsqueda":
                self.data_structure = BinarySearchTree(None)

            for item in items:
                if structure == "Pila":
                    self.data_structure.push(item)
                elif structure == "Cola":
                    self.data_structure.enqueue(item)
                elif structure == "Lista simplemente enlazada":
                    self.data_structure.insert_end(item)
                elif structure == "Lista circular":
                    self.data_structure.insert_end(item)
                elif structure == "Lista doblemente enlazada":
                    self.data_structure.insert_end(item)
                elif structure == "Lista circular doble":
                    self.data_structure.insert_end(item)
                elif structure == "Árbol binario":
                    if self.data_structure.data is None:
                        self.data_structure.data = item
                    else:
                        self.data_structure.insert(item)
                elif structure == "Árbol de búsqueda":
                    if self.data_structure.data is None:
                        self.data_structure.data = item
                    else:
                        self.data_structure.insert(item)

            self.structure_combo.setCurrentText(structure)
            self.data_type_combo.setCurrentText(data_type)
            self.update_data_structure_view()

    def draw_tree_node(self, data, x, y, node_radius=20):
        node = QGraphicsEllipseItem(x - node_radius / 2, y - node_radius / 2, node_radius, node_radius)
        node.setBrush(QBrush(Qt.green))
        self.scene.addItem(node)
        text = QGraphicsTextItem(str(data))
        text_width = text.boundingRect().width()
        text_height = text.boundingRect().height()
        text.setPos(x - text_width / 2, y - text_height / 2)
        self.scene.addItem(text)

    def draw_tree_edges(self, node, x, y, dx, dy):
        if node is None:
            return
        if node.left:
            self.scene.addItem(QGraphicsLineItem(x, y, x - dx, y + dy))
            self.draw_tree_edges(node.left, x - dx, y + dy, dx / 2, dy)
        if node.right:
            self.scene.addItem(QGraphicsLineItem(x, y, x + dx, y + dy))
            self.draw_tree_edges(node.right, x + dx, y + dy, dx / 2, dy)

    def draw_tree(self, tree, x, y, dx):
        if tree is None:
            return
        self.draw_tree_node(tree.data, x, y)
        self.draw_tree_edges(tree.left, x, y, dx / 2, dy)
        self.draw_tree_edges(tree.right, x, y, dx / 2, dy)

    def update_data_structure_view(self):
        self.scene.clear()
        if self.data_structure:
            if isinstance(self.data_structure, Stack) or isinstance(self.data_structure, Queue):
                items = []
                item = self.data_structure.pop() if isinstance(self.data_structure, Stack) else self.data_structure.dequeue()
                while item:
                    items.append(item)
                    item = self.data_structure.pop() if isinstance(self.data_structure, Stack) else self.data_structure.dequeue()
                x, y = 100, 100
                for i, item in enumerate(items):
                    text = QGraphicsTextItem(str(item))
                    text.setPos(x, y + 50 * i)
                    self.scene.addItem(text)
            elif isinstance(self.data_structure, (LinkedList, CircularLinkedList, DoublyLinkedList, CircularDoublyLinkedList)):
                x, y = 100, 100
                current = self.data_structure.head
                while current:
                    text = QGraphicsTextItem(str(current.data))
                    text.setPos(x, y)
                    self.scene.addItem(text)
                    current = current.next
                    y += 50
            elif isinstance(self.data_structure, (BinaryTree, BinarySearchTree)):
                dx = 200
                dy = 100
                self.draw_tree(self.data_structure, 400, 100, dx)
        else:
            self.scene.clear()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = DataStructureApp()
    window.show()
    sys.exit(app.exec_())
