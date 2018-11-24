\* Minimum Cost Flow *\
Minimize
OBJ: 20 A_B + 7 A_C + 4 B_D + 16 B_E + 4 C_D + 3 C_F + 2 D_E + 6 D_F + 18 E_G
 + 9 F_G
Subject To
_C1: A_B + A_C <= 10
_C2: E_G + F_G = 10
_C3: A_B - B_D - B_E = 0
_C4: A_C - C_D - C_F = 0
_C5: B_D + C_D - D_E - D_F = 0
_C6: B_E + D_E - E_G = 0
_C7: C_F + D_F - F_G = 0
Bounds
0 <= A_B <= 20
0 <= A_C <= 15
0 <= B_D <= 4
0 <= B_E <= 21
0 <= C_D <= 4
0 <= C_F <= 9
0 <= D_E <= 2
0 <= D_F <= 10
0 <= E_G <= 24
0 <= F_G <= 10
Generals
A_B
A_C
B_D
B_E
C_D
C_F
D_E
D_F
E_G
F_G
End
