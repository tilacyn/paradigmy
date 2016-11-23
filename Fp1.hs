head' :: [a] -> a
head' (x:_) = x

tail' :: [a] -> [a]
tail' [] = []
tail' (_:xs) = xs

take' :: Int -> [a] -> [a]
take' _ [] = []
take' 0 _ = []
take' n (x:xs) = x:take' (n - 1) xs

drop' :: Int -> [a] -> [a]
drop' _ [] = []
drop' 0 xs = xs
drop' n (_:xs) = drop' (n - 1) xs

filter' :: (a -> Bool) -> [a] -> [a]
filter' _ [] = []
filter' func (x:xs) | func x    = x:filter' func xs
                    | otherwise = filter' func xs

foldl' :: (a -> b -> a) -> a -> [b] -> a
foldl' _ z [] = z
foldl' f z (x:xs) = foldl' f (f z x) xs

concat' :: [a] -> [a] -> [a]
concat' [] ys = ys
concat' (x:xs) ys = x:concat' xs ys
