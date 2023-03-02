function [y] = qween(x1, y1, x2, y2)
    if abs(x1 - x2) == abs(y1 - y2) | x1 == x2 | y1 == y2
        y = 'YES'
    else
        y = 'NO'
    endif
end