

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


def defaultValue():
    """
    @goal : -
    @coverage : -
    """
    test.assert_true_fatal(1==2, "1==2")
    test.assert_true(1==1, "1==1")

        
def start():
    pass

def stop():
    pass


def create():
    raise Exception()




if __name__ == "__main__":
    
    test.set_create(create)
    test.set_setup(start)
    test.add_test_case(defaultValue)
    test.set_cleanup(stop)
    test.run_script()

    
    
    
    
    
    
    
    
    
    


