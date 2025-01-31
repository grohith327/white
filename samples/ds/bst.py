class TreeNode:
  def __init__(    self   ,     key     ):
    self.key     =    key
    self.left   =     None
    self.right   =  None
class BinarySearchTree:
  def __init__( self     ):
    self.root   =   None
  def insert(    self ,  key  ):
    if self.root is None:
      self.root    =   TreeNode(   key )
    else:
      self._insert_recursive(   self.root   ,      key   )
  def _insert_recursive(  self    ,   node    ,  key  ):
    if key    <  node.key:
      if node.left is None:
        node.left     =    TreeNode(   key )
      else:
        self._insert_recursive( node.left    ,      key   )
    elif key    >  node.key:
      if node.right is None:
        node.right    =      TreeNode(  key  )
      else:
        self._insert_recursive(  node.right     ,   key    )
  def search(    self   ,     key  ):
    return self._search_recursive( self.root    ,     key )
  def _search_recursive(     self ,    node    ,      key ):
    if node is None or node.key  ==   key:
      return node
    if key    <      node.key:
      return self._search_recursive( node.left  ,      key    )
    return self._search_recursive(  node.right   ,  key    )
  def inorder_traversal(   self   ):
    result  =  []
    self._inorder_recursive(  self.root    ,      result    )
    return result
  def _inorder_recursive(  self    ,    node  ,    result    ):
    if node:
      self._inorder_recursive( node.left    ,    result    )
      result.append(   node.key     )
      self._inorder_recursive( node.right    ,     result    )
  def preorder_traversal(     self  ):
    result      =   []
    self._preorder_recursive(   self.root ,     result  )
    return result
  def _preorder_recursive(    self     ,      node    ,  result     ):
    if node:
      result.append( node.key    )
      self._preorder_recursive(    node.left   ,   result )
      self._preorder_recursive(     node.right ,    result    )
  def postorder_traversal( self   ):
    result  =  []
    self._postorder_recursive(  self.root  ,  result  )
    return result
  def _postorder_recursive(     self     ,      node    ,      result    ):
    if node:
      self._postorder_recursive(   node.left    ,   result    )
      self._postorder_recursive( node.right     ,    result    )
      result.append(   node.key   )
bst     =      BinarySearchTree(   )
keys     =     [50, 30, 70, 20, 40, 60, 80]
for key in keys:
  bst.insert(     key   )
print(  "In-order traversal:"  ,     bst.inorder_traversal(        )   )
print( "Pre-order traversal:" ,   bst.preorder_traversal(       )    )
print(  "Post-order traversal:"  ,      bst.postorder_traversal(         )  )
search_key   =    60
result  =   bst.search(   search_key   )
if result:
  print(     f"Key {search_key} found in the BST." )
else:
  print( f"Key {search_key} not found in the BST." )
int("In-order traversal:", bst.inorder_traversal())
print("Pre-order traversal:", bst.preorder_traversal())
print("Post-order traversal:", bst.postorder_traversal())

search_key = 60
result = bst.search(search_key)
if result:
    print(f"Key {search_key} found in the BST.")
else:
    print(f"Key {search_key} not found in the BST.")