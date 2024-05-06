import sys
import json
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QComboBox, \
    QLineEdit, QTextEdit, QFileDialog, QMessageBox, QGraphicsView, QGraphicsScene, QInputDialog, QGraphicsRectItem, \
    QGraphicsTextItem, QGraphicsEllipseItem


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
        current = self
        while current.left:
            current = current.left
        return current.data

    def height(self):
        if self.left and self.right:
            return 1 + max(self.left.height(), self.right.height())
        elif self.left:
            return 1 + self.left.height()
        elif self.right:
            return 1 + self.right.height()
        else:
            return 1


class BinarySearchTree(BinaryTree):
    def insert(self, data):
        if self.data:
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


class DataStructureApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Software Educativo de Estructuras de Datos")
        self.setGeometry(100, 100, 800, 600)

        self.layout = QVBoxLayout()

        # Selección de estructura de datos
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
            data_text, ok = QInputDialog.getText(self, "Eliminar dato", "Ingrese el valor lógico (True o False) a eliminar:")
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
            if self.data_structure.peek() == data:
                self.data_structure.pop()
        elif structure == 'Cola':
            if self.data_structure.peek() == data:
                self.data_structure.dequeue()
        elif structure == 'Lista simplemente enlazada':
            pass
        elif structure == 'Lista circular':
            pass
        elif structure == 'Lista doblemente enlazada':
            pass
        elif structure == 'Lista circular doble':
            pass
        elif structure == 'Árbol binario':
            self.data_structure = self.data_structure.delete(data)
        elif structure == 'Árbol de búsqueda':
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
            data_text, ok = QInputDialog.getText(self, "Buscar dato", "Ingrese el valor lógico (True o False) a buscar:")
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

        if not ok:
            return

        structure = self.structure_combo.currentText()
        if structure == 'Pila':
            pass
        elif structure == 'Cola':
            pass
        elif structure == 'Lista simplemente enlazada':
            if self.data_structure.search(data):
                QMessageBox.information(self, "Búsqueda", f"El dato {data} ha sido encontrado en la estructura de datos.")
                return
        elif structure == 'Lista circular':
            if self.data_structure.search(data):
                QMessageBox.information(self, "Búsqueda", f"El dato {data} ha sido encontrado en la estructura de datos.")
                return
        elif structure == 'Lista doblemente enlazada':
            if self.data_structure.search(data):
                QMessageBox.information(self, "Búsqueda", f"El dato {data} ha sido encontrado en la estructura de datos.")
                return
        elif structure == 'Lista circular doble':
            if self.data_structure.search(data):
                QMessageBox.information(self, "Búsqueda", f"El dato {data} ha sido encontrado en la estructura de datos.")
                return
        elif structure == 'Árbol binario':
            if self.data_structure.search(data):
                QMessageBox.information(self, "Búsqueda", f"El dato {data} ha sido encontrado en la estructura de datos.")
                return
        elif structure == 'Árbol de búsqueda':
            if self.data_structure.search(data):
                QMessageBox.information(self, "Búsqueda", f"El dato {data} ha sido encontrado en la estructura de datos.")
                return

        QMessageBox.information(self, "Búsqueda", f"El dato {data} no ha sido encontrado en la estructura de datos.")

    def save_data(self):
        if not self.data_structure:
            return

        file_path, _ = QFileDialog.getSaveFileName(self, "Guardar archivo", "", "Archivos JSON (*.json)")
        if not file_path:
            return

        data = {
            "structure_type": type(self.data_structure).__name__,
            "data": []
        }

        if isinstance(self.data_structure, Stack) or isinstance(self.data_structure, Queue):
            current = self.data_structure.top if isinstance(self.data_structure, Stack) else self.data_structure.front
            while current:
                data["data"].append(current.data)
                current = current.next
        elif isinstance(self.data_structure, (LinkedList, CircularLinkedList, DoublyLinkedList, CircularDoublyLinkedList)):
            current = self.data_structure.head
            while current:
                data["data"].append(current.data)
                current = current.next
                if current == self.data_structure.head:
                    break
        elif isinstance(self.data_structure, BinaryTree) or isinstance(self.data_structure, BinarySearchTree):
            nodes = [self.data_structure]
            while nodes:
                node = nodes.pop(0)
                if node:
                    data["data"].append(node.data)
                    if node.left:
                        nodes.append(node.left)
                    if node.right:
                        nodes.append(node.right)

        with open(file_path, 'w') as f:
            json.dump(data, f)

        QMessageBox.information(self, "Guardar archivo", "Estructura de datos guardada exitosamente.")

    def load_data(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Cargar archivo", "", "Archivos JSON (*.json)")
        if not file_path:
            return

        with open(file_path, 'r') as f:
            data = json.load(f)

        if data["structure_type"] == 'Stack':
            self.data_structure = Stack()
            for item in data["data"]:
                self.data_structure.push(item)
        elif data["structure_type"] == 'Queue':
            self.data_structure = Queue()
            for item in data["data"]:
                self.data_structure.enqueue(item)
        elif data["structure_type"] == 'LinkedList':
            self.data_structure = LinkedList()
            for item in data["data"]:
                self.data_structure.insert_end(item)
        elif data["structure_type"] == 'CircularLinkedList':
            self.data_structure = CircularLinkedList()
            for item in data["data"]:
                self.data_structure.insert_end(item)
        elif data["structure_type"] == 'DoublyLinkedList':
            self.data_structure = DoublyLinkedList()
            for item in data["data"]:
                self.data_structure.insert_end(item)
        elif data["structure_type"] == 'CircularDoublyLinkedList':
            self.data_structure = CircularDoublyLinkedList()
            for item in data["data"]:
                self.data_structure.insert_end(item)
        elif data["structure_type"] == 'BinaryTree':
            self.data_structure = BinaryTree(data["data"][0])
            for item in data["data"][1:]:
                self.data_structure.insert(item)
        elif data["structure_type"] == 'BinarySearchTree':
            self.data_structure = BinarySearchTree(data["data"][0])
            for item in data["data"][1:]:
                self.data_structure.insert(item)

        self.update_data_structure_view()

    def update_data_structure_view(self):
        self.scene.clear()

        if not self.data_structure:
            return

        structure_type = type(self.data_structure).__name__
        if structure_type in ['Stack', 'Queue']:
            current = self.data_structure.top if structure_type == 'Stack' else self.data_structure.front
            y = 50
            while current:
                node = QGraphicsRectItem(0, y, 100, 50)
                text = QGraphicsTextItem(str(current.data))
                text.setPos(10, y + 10)
                self.scene.addItem(node)
                self.scene.addItem(text)
                y += 70
                current = current.next
        elif structure_type in ['LinkedList', 'CircularLinkedList', 'DoublyLinkedList', 'CircularDoublyLinkedList']:
            current = self.data_structure.head
            y = 50
            while current:
                node = QGraphicsRectItem(0, y, 100, 50)
                text = QGraphicsTextItem(str(current.data))
                text.setPos(10, y + 10)
                self.scene.addItem(node)
                self.scene.addItem(text)
                y += 70
                current = current.next
                if current == self.data_structure.head:
                    break
        elif structure_type in ['BinaryTree', 'BinarySearchTree']:
            self.draw_binary_tree(self.data_structure, self.data_structure.height() * 50, 0, 400)

    def draw_binary_tree(self, node, y, x, space):
        if not node:
            return
        circle = QGraphicsEllipseItem(x, y, 50, 50)
        text = QGraphicsTextItem(str(node.data))
        text.setPos(x + 10, y + 10)
        self.scene.addItem(circle)
        self.scene.addItem(text)
        if node.left:
            self.scene.addLine(x + 25, y + 50, x - space + 25, y + 100)
            self.draw_binary_tree(node.left, y + 100, x - space, space / 2)
        if node.right:
            self.scene.addLine(x + 25, y + 50, x + space + 25, y + 100)
            self.draw_binary_tree(node.right, y + 100, x + space, space / 2)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = DataStructureApp()
    window.show()
    sys.exit(app.exec_())
