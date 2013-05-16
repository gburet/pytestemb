# -*- coding: UTF-8 -*-

"""
PyTestEmb Project : valid manages script execution
"""

__author__      = "$Author: jmbeguinet $"
__copyright__   = "Copyright 2009, The PyTestEmb Project"
__license__     = "GPL"
__email__       = "jm.beguinet@gmail.com"




import sys
import inspect


import pytestemb.utils as utils
import pytestemb.result as result
import pytestemb.pexception as pexception


# redirect sys.stderr => sys.stdout
sys.stderr = sys.stdout






class Valid:
    
    __single = None
    
    def __init__(self, inst_result):
        self._result = inst_result
        self._setup      = self._nothing_
        self._cleanup    = self._nothing_
        self._create     = self._nothing_
        self._destroy    = self._nothing_
        self._case = []
        self._name = utils.get_script_name()
        
        self._aborted = False
        
        self._abort_fatal_mode = False
        self._abort_fatal = False
        
        self._case_name = None

    @classmethod
    def create(cls, inst_result):
        cls.__single = cls(inst_result)
        return cls.__single
    
    @classmethod
    def get(cls):
        return cls.__single 
            

    def _nothing_(self):
        pass

    def set_setup(self, funcsetup):
        if self._setup == self._nothing_ :
            self._setup = funcsetup
        else:
            # Avoid user mistake with two time function set
            raise pexception.PytestembError("Setup function already set")


    def set_cleanup(self, funccleanup):
        if self._cleanup == self._nothing_ :
            self._cleanup = funccleanup
        else:
            # Avoid user mistake with two time function set
            raise pexception.PytestembError("CleanUp function already set")


    def set_create(self, funccreate):
        if self._create == self._nothing_ :
            self._create = funccreate
        else:
            # Avoid user mistake with two time function set
            raise pexception.PytestembError("funcCreate function already set")
        

    def set_destroy(self, funcdestroy):
        if self._destroy == self._nothing_ :
            self._destroy = funcdestroy
        else:
            # Avoid user mistake with two time function set
            raise pexception.PytestembError("funcDestroy function already set")
    
    def set_fatal_mode(self, stop_case_run):
        self._abort_fatal_mode = stop_case_run
        
        

    def add_test_case(self, funccase):
        self._case.append(funccase)


    def get_case_name(self):
        return self._case_name


    def run_script(self):
        self._result.script_start({"name":self._name})
        # Create 
        if self._create == self._nothing_:
            pass
        else:
            self._result.create_start({})
            self.run_try(self._create)
            self._result.create_stop({})
        # Setup
        if self._setup == self._nothing_:
            pass
        else:
            self._result.setup_start({})
            self._case_name = "setup"
            self.run_try(self._setup)
            self._result.setup_stop({})
            self._case_name = None
        # Case
        for acase in self._case :
            name = acase.func_name
            self._result.case_start({"name":name})
            self._case_name = name
            self.run_case(acase)
            self._result.case_stop({"name":name})
            self._case_name = None
        # Cleanup
        if self._cleanup == self._nothing_:
            pass
        else:
            self._result.cleanup_start({})
            self._case_name = "cleanup"
            self.run_try(self._cleanup)
            self._result.cleanup_stop({})
            self._case_name = None
        # Destroy    
        if self._destroy == self._nothing_:
            pass
        else:
            self._result.destroy_start({})
            self.run_try(self._destroy, force=True)
            self._result.destroy_stop({})
    
        self._result.script_stop({"name":self._name})


    def run_try(self, func, force=False):
        
        if self._aborted and not force:
            self._result.aborted({})
            return

        try:
            func()
        except result.TestErrorFatal:
            pass
        except result.TestAbort:
            self._aborted = True                  
        except (Exception), (error):
            self.inspect_traceback(error)


    def run_case(self, case):
        
        if self._aborted or self._abort_fatal:
            self._result.aborted({})
            return
        try:
            case()
        except result.TestErrorFatal:
            if self._abort_fatal_mode:
                self._abort_fatal = True          
        except result.TestAbort:
            self._aborted = True        
        except (Exception), (error):
            self.inspect_traceback(error)
 
 

    def inspect_traceback(self, exception):
        CALL_DEPTH = 1
        DEFAULT = dict.fromkeys(["path", "line", "function", "code"], "no info")
        traceback = inspect.trace()
        stack = []
        

        try :
            for index in range(CALL_DEPTH, len(traceback)):
                stack.append(dict(DEFAULT))
                stack[-1]["path"]      = traceback[index][1]
                stack[-1]["line"]      = traceback[index][2]
                stack[-1]["function"]  = traceback[index][3]
                stack[-1]["code"]      = utils.to_unicode(traceback[index][4][0].strip("\n"))
        except Exception:
            pass

        des = {}
        des["stack"]            = stack
        des["exception_info"]   = utils.to_unicode(exception)
        des["exception_class"]  = exception.__class__.__name__

        self._result.py_exception(des)






