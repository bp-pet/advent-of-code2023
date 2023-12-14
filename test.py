import numpy as np

a = np.array([["a", "b", "c"], ["d", "e", "f"], ["d", "e", "f"]])
b = np.array([["d", "e", "f"], ["d", "e", "f"], ["d", "e", "f"]])
c = np.array([["a", "e", "f"], ["d", "e", "f"], ["d", "e", "f"]])

l = [a, b]

# print((np.array(["d", "e"]) in l))

new = np.concatenate([np.array([a]), np.array([b])], axis=0)
print(new.shape)

# np.any(np.all(b == new, axis=(1, 2)))

# print(np.isin(a, l))

print(c in new)