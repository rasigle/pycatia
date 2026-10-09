from pyv5.knowledge_interfaces.bool_param import BoolParam
from pyv5.knowledge_interfaces.free_parameter import FreeParameter
from pyv5.knowledge_interfaces.int_param import IntParam
from pyv5.knowledge_interfaces.list_parameter import ListParameter
from pyv5.knowledge_interfaces.parameter import Parameter
from pyv5.knowledge_interfaces.real_param import RealParam
from pyv5.knowledge_interfaces.str_param import StrParam

AnyParameter = (
    BoolParam
    | FreeParameter
    | IntParam
    | ListParameter
    | Parameter
    | RealParam
    | StrParam
)
