function [y] = Leapyear(i)
    if (mod(i,4) == 0 & mod(i,100) ~= 0) | mod(i,400) == 0
        y = 'YES'
    else
        y = 'NO'
    endif
end