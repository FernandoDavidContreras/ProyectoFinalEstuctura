import sys
import json
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QComboBox, \
    QLineEdit, QTextEdit, QFileDialog, QMessageBox, QGraphicsView, QGraphicsScene, QInputDialog, QGraphicsRectItem, \
    QGraphicsTextItem, QGraphicsEllipseItem


class Node:
    def __init__(self, data):
        self.data = data
        self.next = None


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