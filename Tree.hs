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
delete k (Node key val EmptyTree right)
    | k == key = right
delete k (Node key val left EmptyTree)
    | k == key = left
delete k (Node key val left (Node kr vr EmptyTree rright))
    | k == key = Node kr vr left rright
delete k (Node key val left (Node kr vr (Node krl vrl rlleft rlright) rright))
    | k == key = Node krl vrl left (Node kr vr (delete krl (Node krl vrl rlleft rlright)) rright)
