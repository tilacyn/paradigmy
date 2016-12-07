import Prelude hiding (lookup)
data BinaryTree k v = EmptyTree | Node k v (BinaryTree k v) (BinaryTree k v) deriving Show
     
insert :: (Ord k) => k -> v -> BinaryTree k v -> BinaryTree k v    
insert k v EmptyTree = Node k v EmptyTree EmptyTree 
insert k v (Node key val left right)     
    | k == key = Node k v left right    
    | k < key  = Node key val (insert k v left) right    
    | k > key  = Node key val left (insert k v right)

lookup :: Ord k => k -> BinaryTree k v -> Maybe v
lookup k EmptyTree = Nothing
lookup k (Node key val left right)
    | k == key = Just val
    | k < key = lookup k left
    | k > key = lookup k right

delete :: Ord k => k -> BinaryTree k v -> BinaryTree k v
delete k EmptyTree = EmptyTree
delete k (Node key val left right)
    | k < key = Node key val (delete k left) right
    | k > key = Node key val left (delete k right)
    | k == key = merge left right

merge :: BinaryTree k v -> BinaryTree k v -> BinaryTree k v
merge EmptyTree right = right
merge (Node k v l r) other = Node k v l (merge r other)
