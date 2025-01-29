# Code generated from DeepSeek

class TreeNode:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None
        self.height = 1  # Height of the node (used for balancing)

class AVLTree:
    def __init__(self):
        self.root = None

    def insert(self, key):
        """Public method to insert a key into the AVL tree."""
        self.root = self._insert(self.root, key)

    def _insert(self, node, key):
        """Recursive helper method to insert a key into the AVL tree."""
        # Step 1: Perform standard BST insertion
        if not node:
            return TreeNode(key)
        elif key < node.key:
            node.left = self._insert(node.left, key)
        else:
            node.right = self._insert(node.right, key)

        # Step 2: Update the height of the ancestor node
        node.height = 1 + max(self._get_height(node.left), self._get_height(node.right))

        # Step 3: Get the balance factor to check if the node became unbalanced
        balance = self._get_balance(node)

        # Step 4: Rebalance the tree if necessary
        # Left Left Case
        if balance > 1 and key < node.left.key:
            return self._right_rotate(node)

        # Right Right Case
        if balance < -1 and key > node.right.key:
            return self._left_rotate(node)

        # Left Right Case
        if balance > 1 and key > node.left.key:
            node.left = self._left_rotate(node.left)
            return self._right_rotate(node)

        # Right Left Case
        if balance < -1 and key < node.right.key:
            node.right = self._right_rotate(node.right)
            return self._left_rotate(node)

        return node

    def _get_height(self, node):
        """Helper method to get the height of a node."""
        if not node:
            return 0
        return node.height

    def _get_balance(self, node):
        """Helper method to get the balance factor of a node."""
        if not node:
            return 0
        return self._get_height(node.left) - self._get_height(node.right)

    def _left_rotate(self, z):
        """Perform a left rotation."""
        y = z.right
        T2 = y.left

        # Perform rotation
        y.left = z
        z.right = T2

        # Update heights
        z.height = 1 + max(self._get_height(z.left), self._get_height(z.right))
        y.height = 1 + max(self._get_height(y.left), self._get_height(y.right))

        # Return the new root
        return y

    def _right_rotate(self, z):
        """Perform a right rotation."""
        y = z.left
        T3 = y.right

        # Perform rotation
        y.right = z
        z.left = T3

        # Update heights
        z.height = 1 + max(self._get_height(z.left), self._get_height(z.right))
        y.height = 1 + max(self._get_height(y.left), self._get_height(y.right))

        # Return the new root
        return y

    def inorder_traversal(self):
        """
        Public method to perform an inorder traversal of the AVL tree.
        """
        result = []
        self._inorder_traversal(self.root, result)
        return result

    def _inorder_traversal(self, node, result):
        """Recursive helper method for inorder traversal."""
        if node:
            self._inorder_traversal(node.left, result)
            result.append(node.key)
            self._inorder_traversal(node.right, result)

    def search(self, key):
        """Public method to search for a key in the AVL tree."""
        return self._search(self.root, key)

    def _search(self, node, key):
        """Recursive helper method to search for a key in the AVL tree."""
        if not node or node.key == key:
            return node
        if key < node.key:
            return self._search(node.left, key)
        return self._search(node.right, key)

    def delete(self, key):
        """Public method to delete a key from the AVL tree."""
        self.root = self._delete(self.root, key)

    def _delete(self, node, key):
        """Recursive helper method to delete a key from the AVL tree."""
        # Step 1: Perform standard BST delete
        if not node:
            return node
        elif key < node.key:
            node.left = self._delete(node.left, key)
        elif key > node.key:
            node.right = self._delete(node.right, key)
        else:
            # Node with only one child or no child
            if not node.left:
                return node.right
            elif not node.right:
                return node.left
            # Node with two children: Get the inorder successor (smallest in the right subtree)
            temp = self._get_min_value_node(node.right)
            node.key = temp.key
            node.right = self._delete(node.right, temp.key)

        # If the tree had only one node, return
        if not node:
            return node

        # Step 2: Update the height of the current node
        node.height = 1 + max(self._get_height(node.left), self._get_height(node.right))

        # Step 3: Get the balance factor to check if the node became unbalanced
        balance = self._get_balance(node)

        # Step 4: Rebalance the tree if necessary
        # Left Left Case
        if balance > 1 and self._get_balance(node.left) >= 0:
            return self._right_rotate(node)

        # Right Right Case
        if balance < -1 and self._get_balance(node.right) <= 0:
            return self._left_rotate(node)

        # Left Right Case
        if balance > 1 and self._get_balance(node.left) < 0:
            node.left = self._left_rotate(node.left)
            return self._right_rotate(node)

        # Right Left Case
        if balance < -1 and self._get_balance(node.right) > 0:
            node.right = self._right_rotate(node.right)
            return self._left_rotate(node)

        return node

    def _get_min_value_node(self, node):
        """Helper method to get the node with the minimum key in a subtree."""
        current = node
        while current.left:
            current = current.left
        return current
    
avl = AVLTree()
keys = [10, 20, 30, 40, 50, 25]

# Insert keys
for key in keys:
    avl.insert(key)

# Inorder traversal (should print sorted keys)
print("Inorder Traversal:", avl.inorder_traversal())

# Search for a key
print("Search for 30:", avl.search(30) is not None)

# Delete a key
avl.delete(30)
print("Inorder Traversal after deleting 30:", avl.inorder_traversal())