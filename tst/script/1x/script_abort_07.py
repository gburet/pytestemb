

"""
@goal: -
@todo: -
@warning: -
@requires: -
@precondition: -
@postcondition: -
"""



import pytestemb as test


import time



def create():
    pass

def destroy():
    test.abort()

        
def setup():
    pass

def cleanup():
    pass


def case_01():
    pass

def case_02():
    pass

def case_03():
    pass




if __name__ == "__main__":
    

    test.set_setup(setup)
    test.set_create(create)
    test.add_test_case(case_01)
    test.add_test_case(case_02)
    test.add_test_case(case_03)
    test.set_cleanup(cleanup)
    test.set_destroy(destroy)
    test.run_script()

    
    
    
    
    
    
    
    
    
    


