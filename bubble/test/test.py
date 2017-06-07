# -*- coding:utf-8 -*-

class Base:
    base_name = 'BSession'

    #程序id
    base_id = 0

    base_ref = base_name + '_' + str(base_id)

class Base_0:
    base_name = 'BSession'

    #程序id
    base_id = 0

    base_ref = Base.base_ref


print Base.base_name
print Base.base_id
print Base_0.base_ref

