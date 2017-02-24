function[newX] = reduce(X, dim)
%center data, run svd
x_centered = X - mean(mean(X));
x_centered = x_centered.';
[U, V, D] = svd(x_centered, 0);

%reduce dimensions to 50
 U = U(:, 1:dim);
 V = V(1:dim, :);

%reconstruct
newX = U*V*D.';
%newX = V*X;

newX = newX.';

end