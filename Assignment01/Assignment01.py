import pathlib
import math
def load_system(path: pathlib.Path) -> tuple[list[list[float]], list[float]]:
    names="xyz"
    A = []
    B = []
    
    with open(path) as file:
        for line in file:
            line = line.strip()
            if line == "":
                continue

            left, right = line.split("=")
            left = left.replace(" ", "")
            sign = 1
            num = ""
            row=[0.0]*len(names)
            for ch in left:
                if ch == "-":
                    sign = -1
                elif ch == "+":
                    sign = 1
                elif ch.isdigit() or ch == ".":
                    num += ch
                else:                    # variable letter: the term is finished
                    value = float(num) if num else 1.0
                    row[names.index(ch)]+=(sign * value)
                    sign = 1
                    num = ""

            A.append(row)
            B.append(float(right))
    return A, B


A, B = load_system(pathlib.Path("input.txt"))
print(f"{A=} {B=}")


def determinant(matrix: list[list[float]]) -> float:
    det=matrix[0][0]*(matrix[1][1]*matrix[2][2]-matrix[1][2]*matrix[2][1])-matrix[0][1]*(matrix[1][0]*matrix[2][2]-matrix[1][2]*matrix[2][0])+matrix[0][2]*(matrix[1][0]*matrix[2][1]-matrix[1][1]*matrix[2][0])
    return det
print(f"{determinant(A)=}")

def trace(matrix: list[list[float]]) -> float:
    trace=matrix[0][0]+matrix[1][1]+matrix[2][2]
    return trace
print(f"{trace(A)=}")

def norm(vector: list[float]) -> float:
    return math.sqrt(vector[0]*vector[0]+vector[1]*vector[1]+vector[2]*vector[2])
print(f"{norm(B)=}")

def transpose(matrix: list[list[float]]) -> list[list[float]]:
    tr_matrix = [[0.0] * len(matrix) for _ in range(len(matrix))]
    for i in range(len(matrix)):
        for j in range(len(matrix)):
            tr_matrix[j][i]=matrix[i][j]
    return tr_matrix
print(f"{transpose(A)=}")

def multiply(matrix: list[list[float]], vector: list[float]) -> list[float]:
    result=[]
    for i in range(len(matrix)):
        coef=0
        for j in range(len(matrix)):
            coef+=vector[j]*matrix[i][j]
        result.append(coef)
    return result
print(f"{multiply(A, B)=}")

def replace_column(matrix: list[list[float]], vector: list[float],index:int) -> list[list[float]]:
    new_matrix=[row[:] for row in matrix]
    for j in range(len(new_matrix)):
        new_matrix[j][index]=vector[j]
    return new_matrix
    
def solve_cramer(matrix: list[list[float]], vector: list[float]) -> list[float]:
    det = determinant(matrix)
    if abs(det) < 1e-9:
        raise ValueError("determinant is 0, Cramer's rule does not apply")

    result=[]
    for i in range(len(matrix)):
        coef=determinant(replace_column(matrix,vector,i))/det
        result.append(coef)
    return result
print(f"{solve_cramer(A, B)=}")

def minor(matrix: list[list[float]], i: int, j: int) -> list[list[float]]:
    result=[]
    for row in range (len(matrix)):
        if row==i:
            continue
        coef=[]
        for col in range(len(matrix)):
            if(row!=i and col!=j):
                coef.append(matrix[row][col])
        result.append(coef)
    return result
def det_minor(matrix:list[list[float]])->float:
    return matrix[0][0]*matrix[1][1]-matrix[0][1]*matrix[1][0]  

def cofactor(matrix: list[list[float]]) -> list[list[float]]:
    new_matrix=[]
    for i in range (len(matrix)):
        coef=[]
        for j in range (len(matrix)):
            if((i+j)%2==0):
                coef.append(det_minor(minor(matrix,i,j)))
            else:
                coef.append(-1.0*det_minor(minor(matrix,i,j)))   
        new_matrix.append(coef)
    return new_matrix   
   
def inverse(matrix: list[list[float]]) -> list[list[float]]:
    det = determinant(matrix)
    if abs(det) < 1e-9:
        raise ValueError("determinant is 0, can't compute the inverse")
    new_matrix=transpose(cofactor(matrix))
    for i in range (len(matrix)):
         for j in range (len(matrix)):
             new_matrix[i][j]=new_matrix[i][j]*(1/det)
    return new_matrix
 
def solve(matrix: list[list[float]], vector: list[float]) -> list[float]:
    return multiply(inverse(matrix),vector)      
print(f"{solve(A, B)=}")