function [y] = year_x(year)
    if (mod(year, 4) == 0) & (mod(year,100) ~= 0) | (mod(year, 400) == 0)
        y = 'YES'
    else
        y='NO'
end
