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
            try:
                data = int(data_text) if ok else None
            except ValueError:
                data = None
        elif data_type == 'Números flotantes':
            data_text, ok = QInputDialog.getText(self, "Insertar dato", "Ingrese el número flotante:")
            try:
                data = float(data_text) if ok else None
            except ValueError:
                data = None
        elif data_type == 'Valores lógicos':
            data_text, ok = QInputDialog.getText(self, "Insertar dato", "Ingrese el valor lógico (True o False):")
            data = data_text.lower() == 'true' if ok else None
        elif data_type == 'Cadenas de texto':
            data_text, ok = QInputDialog.getText(self, "Insertar dato", "Ingrese la cadena de texto:")
            data = str(data_text) if ok else None
        else:
            data = None

        if data is None:
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
                try:
                    data = int(data_text) if ok else None
                except ValueError:
                    data = None
                if data is None:
                    return
                self.data_structure = BinaryTree(data)
            else:
                self.data_structure.insert(data)
        elif structure == 'Árbol de búsqueda':
            if not self.data_structure:
                data_text, ok = QInputDialog.getText(self, "Insertar dato", "Ingrese el número entero para la raíz del árbol:")
                try:
                    data = int(data_text) if ok else None
                except ValueError:
                    data = None
                if data is None:
                    return
                self.data_structure = BinarySearchTree(data)
            else:
                self.data_structure.insert(data)

        self.update_data_structure_view()

    def delete_data(self):
        if not self.data_structure:
            return

        data_type = self.data_type_combo.currentText()
        if data_type == 'Números enteros':
            data_text, ok = QInputDialog.getText(self, "Eliminar dato", "Ingrese el número entero a eliminar:")
            try:
                data = int(data_text) if ok else None
            except ValueError:
                data = None
        elif data_type == 'Números flotantes':
            data_text, ok = QInputDialog.getText(self, "Eliminar dato", "Ingrese el número flotante a eliminar:")
            try:
                data = float(data_text) if ok else None
            except ValueError:
                data = None
        elif data_type == 'Valores lógicos':
            data_text, ok = QInputDialog.getText(self, "Eliminar dato", "Ingrese el valor lógico (True o False) a eliminar:")
            data = data_text.lower() == 'true' if ok else None
        elif data_type == 'Cadenas de texto':
            data_text, ok = QInputDialog.getText(self, "Eliminar dato", "Ingrese la cadena de texto a eliminar:")
            data = str(data_text) if ok else None
        else:
            data = None

        if data is None:
            return

        if isinstance(self.data_structure, (BinaryTree, BinarySearchTree)):
            self.data_structure = self.data_structure.delete(data)
        else:
            structure = self.structure_combo.currentText()
            if structure == 'Pila':
                if isinstance(self.data_structure, Stack):
                    if self.data_structure.peek() == data:
                        self.data_structure.pop()
            elif structure == 'Cola':
                if isinstance(self.data_structure, Queue):
                    if self.data_structure.peek() == data:
                        self.data_structure.dequeue()
            elif structure in ['Lista simplemente enlazada', 'Lista circular', 'Lista doblemente enlazada', 'Lista circular doble']:
                pass  # to be implemented

        self.update_data_structure_view()

    def search_data(self):
        if not self.data_structure:
            return

        data_type = self.data_type_combo.currentText()
        if data_type == 'Números enteros':
            data_text, ok = QInputDialog.getText(self, "Buscar dato", "Ingrese el número entero a buscar:")
            try:
                data = int(data_text) if ok else None
            except ValueError:
                data = None
        elif data_type == 'Números flotantes':
            data_text, ok = QInputDialog.getText(self, "Buscar dato", "Ingrese el número flotante a buscar:")
            try:
                data = float(data_text) if ok else None
            except ValueError:
                data = None
        elif data_type == 'Valores lógicos':
            data_text, ok = QInputDialog.getText(self, "Buscar dato", "Ingrese el valor lógico (True o False) a buscar:")
            data = data_text.lower() == 'true' if ok else None
        elif data_type == 'Cadenas de texto':
            data_text, ok = QInputDialog.getText(self, "Buscar dato", "Ingrese la cadena de texto a buscar:")
            data = str(data_text) if ok else None
        else:
            data = None

        if data is None:
            return

        if isinstance(self.data_structure, (BinaryTree, BinarySearchTree)):
            result = self.data_structure.search(data)
        else:
            structure = self.structure_combo.currentText()
            if structure == 'Pila':
                if isinstance(self.data_structure, Stack):
                    result = data in [self.data_structure.peek()]
            elif structure == 'Cola':
                if isinstance(self.data_structure, Queue):
                    result = data in [self.data_structure.peek()]
            elif structure in ['Lista simplemente enlazada', 'Lista circular', 'Lista doblemente enlazada', 'Lista circular doble']:
                if isinstance(self.data_structure, (LinkedList, CircularLinkedList, DoublyLinkedList, CircularDoublyLinkedList)):
                    result = self.data_structure.search(data)

        if result:
            QMessageBox.information(self, "Resultado de la búsqueda", f"El dato {data} fue encontrado.")
        else:
            QMessageBox.information(self, "Resultado de la búsqueda", f"El dato {data} no fue encontrado.")

    def save_data(self):
        if not self.data_structure:
            return

        file_path, _ = QFileDialog.getSaveFileName(self, "Guardar estructura de datos", "", "JSON Files (*.json)")
        if not file_path:
            return

        structure = self.structure_combo.currentText()

        if structure in ['Pila', 'Cola']:
            saved_data = []
            if isinstance(self.data_structure, Stack):
                temp_stack = Stack()
                while self.data_structure.peek() is not None:
                    saved_data.append(self.data_structure.peek())
                    temp_stack.push(self.data_structure.pop())
                while temp_stack.peek() is not None:
                    self.data_structure.push(temp_stack.pop())
            elif isinstance(self.data_structure, Queue):
                temp_queue = Queue()
                while self.data_structure.peek() is not None:
                    saved_data.append(self.data_structure.peek())
                    temp_queue.enqueue(self.data_structure.dequeue())
                while temp_queue.peek() is not None:
                    self.data_structure.enqueue(temp_queue.dequeue())
        elif structure in ['Lista simplemente enlazada', 'Lista circular', 'Lista doblemente enlazada', 'Lista circular doble']:
            if isinstance(self.data_structure, (LinkedList, CircularLinkedList, DoublyLinkedList, CircularDoublyLinkedList)):
                saved_data = []
                current = self.data_structure.head
                while current:
                    saved_data.append(current.data)
                    current = current.next
        elif structure in ['Árbol binario', 'Árbol de búsqueda']:
            saved_data = self.tree_to_dict(self.data_structure)

        with open(file_path, 'w') as f:
            json.dump(saved_data, f, indent=4)

    def load_data(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Cargar estructura de datos", "", "JSON Files (*.json)")
        if not file_path:
            return

        with open(file_path, 'r') as f:
            loaded_data = json.load(f)

        structure = self.structure_combo.currentText()

        if structure in ['Pila', 'Cola']:
            if isinstance(self.data_structure, Stack):
                self.data_structure = Stack()
                for item in loaded_data:
                    self.data_structure.push(item)
            elif isinstance(self.data_structure, Queue):
                self.data_structure = Queue()
                for item in loaded_data:
                    self.data_structure.enqueue(item)
        elif structure in ['Lista simplemente enlazada', 'Lista circular', 'Lista doblemente enlazada', 'Lista circular doble']:
            if isinstance(self.data_structure, (LinkedList, CircularLinkedList, DoublyLinkedList, CircularDoublyLinkedList)):
                self.data_structure = CircularDoublyLinkedList() if structure == 'Lista circular doble' else CircularLinkedList() if structure == 'Lista circular' else \
                    DoublyLinkedList() if structure == 'Lista doblemente enlazada' else LinkedList()
                for item in loaded_data:
                    self.data_structure.insert_end(item)
        elif structure in ['Árbol binario', 'Árbol de búsqueda']:
            if isinstance(self.data_structure, (BinaryTree, BinarySearchTree)):
                self.data_structure = self.dict_to_tree(loaded_data)

        self.update_data_structure_view()

    def tree_to_dict(self, root):
        if not root:
            return None
        return {
            'data': root.data,
            'left': self.tree_to_dict(root.left),
            'right': self.tree_to_dict(root.right)
        }

    def dict_to_tree(self, root_dict):
        if root_dict is None:
            return None
        root = BinaryTree(root_dict['data'])
        root.left = self.dict_to_tree(root_dict['left'])
        root.right = self.dict_to_tree(root_dict['right'])
        return root

    def draw_tree(self, root, x, y, x_space, node_radius=20):
        if root is None:
            return
        self.draw_tree_node(root.data, x, y, node_radius)
        if root.left:
            x_space = x_space // 2
            self.draw_line(x, y, x - x_space, y + 60, root.left.data)
            self.draw_tree(root.left, x - x_space, y + 60, x_space)
        if root.right:
            x_space = x_space // 2
            self.draw_line(x, y, x + x_space, y + 60, root.right.data)
            self.draw_tree(root.right, x + x_space, y + 60, x_space)

    def draw_tree_node(self, data, x, y, node_radius=20):
        node = QGraphicsEllipseItem(x - node_radius / 2, y - node_radius / 2, node_radius, node_radius)
        node.setBrush(QBrush(Qt.green))
        self.scene.addItem(node)
        text = QGraphicsTextItem(str(data))
        text_width = text.boundingRect().width()
        text_height = text.boundingRect().height()
        text.setPos(x - text_width / 2, y - text_height / 2)
        self.scene.addItem(text)

    def draw_line(self, x1, y1, x2, y2, data):
        line = QGraphicsLineItem(x1, y1, x2, y2)
        self.scene.addItem(line)
        text = QGraphicsTextItem(str(data))
        text.setPos((x1 + x2) / 2, (y1 + y2) / 2)
        self.scene.addItem(text)

    def update_data_structure_view(self):
        self.scene.clear()
        if isinstance(self.data_structure, (Stack, Queue)):
            current = self.data_structure.top if isinstance(self.data_structure, Stack) else self.data_structure.front
            x = 50
            y = 50
            while current:
                self.draw_tree_node(current.data, x, y)
                if isinstance(self.data_structure, Stack):
                    current = current.next
                    y += 60
                else:
                    current = current.next
                    x += 60
        elif isinstance(self.data_structure, (LinkedList, CircularLinkedList, DoublyLinkedList, CircularDoublyLinkedList)):
            current = self.data_structure.head
            x = 50
            y = 50
            while current:
                self.draw_tree_node(current.data, x, y)
                current = current.next
                x += 60
        elif isinstance(self.data_structure, (BinaryTree, BinarySearchTree)):
            x = 400
            y = 50
            x_space = 200
            self.draw_tree(self.data_structure, x, y, x_space)

        self.data_structure_view.setScene(self.scene)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = DataStructureApp()
    window.show()
    sys.exit(app.exec_())
