head' :: [a] -> a
head' (x:xs) = x

tail' :: [a] -> [a]
tail' (x:xs) = xs

take' :: Int -> [a] -> [a]
take' x [] = []
take' 0 xs = []
take' n (x:xs) = x:take' (n - 1) xs

drop' :: Int -> [a] -> [a]
drop' x [] = []
drop' 0 xs = xs
drop' n (x:xs) = drop' (n - 1) xs

filter' :: (a -> Bool) -> [a] -> [a]
filter' func [] = []
filter' func xs | func (head' xs) = (head' xs):filter' func (tail' xs)
                    | otherwise =  filter' func (tail' xs)

foldl' :: (a -> b -> a) -> a -> [b] -> a
foldl' f z [] = z
foldl' f z l = foldl' f (f z (head' l)) (tail' l)

concat' :: [a] -> [a] -> [a]
concat' [] [] = []
concat' [] (l2) = (head' l2):concat' [] (tail' l2)
concat' l1 l2 = (head' l1):concat' (tail' l1) l2

