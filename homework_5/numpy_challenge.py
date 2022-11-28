import numpy as np


if __name__ == "__main__":
    arr1 = np.arange(1,11)
    np.random.seed(993)
    arr2 = np.random.random(7)
    arr3 = np.array([4, 8, 15, 16, 23, 42])


def  matrix_multiplication(matrix1, matrix2):
    return np.matmul(matrix1, matrix2)


def multiplication_check(matrix_list):
    switcher = True
    for i in range(len(matrix_list)-1):
        if matrix_list[i].shape[int(switcher)] != matrix_list[i+1].shape[int(not switcher)]:
            return False
        switcher = not switcher
    return True


def multiply_matrices(matrix_list):
    if multiplication_check(matrix_list) == True:
        if len(matrix_list) > 1:
            new_matrix = matrix_multiplication(matrix_list[0], matrix_list[1])
            matrix_list[1] = new_matrix
            matrix_list.pop(0)
            multiply_matrices(matrix_list)
        if len(matrix_list) == 1:
            return matrix_list[0]
    return None


def compute_2d_distance(point1, point2):
    return np.linalg.norm(point1-point2)


def compute_multidimensional_distance(point1, point2):
    return np.linalg.norm(point1-point2)


def compute_pair_distances(matrix):
    pair_matrix = np.zeros((array.shape[0],array.shape[0]))
    for i in range(array.shape[0]):
        for j in range(array.shape[0]):
            pair_matrix[i, j] = compute_multidimensional_distance(array[i], array[j])
    return pair_matrix