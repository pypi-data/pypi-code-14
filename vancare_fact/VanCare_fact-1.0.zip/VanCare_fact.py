def VanCare_fact(n):             #n的阶乘
    if n==1:
        return 1
    return VanCare_fact(n-1)*n
