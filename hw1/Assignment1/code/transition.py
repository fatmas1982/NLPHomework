class Transition(object):
    """
    This class defines a set of transitions which are applied to a
    configuration to get the next configuration.
    """
    # Define set of transitions
    LEFT_ARC = 'LEFTARC'
    RIGHT_ARC = 'RIGHTARC'
    SHIFT = 'SHIFT'
    REDUCE = 'REDUCE'

    def __init__(self):
        raise ValueError('Do not construct this object!')

    @staticmethod
    def left_arc(conf, relation):
        """
            :param configuration: is the current configuration
            :return : A new configuration or -1 if the pre-condition is not satisfied
        """
        #print(conf)
        #raise NotImplementedError('Please implement left_arc!')
        stack_at_root = conf.stack and conf.stack[-1] == 0
        next_already_dep = conf.stack and len([x for x in conf.arcs if x[2] == conf.stack[-1]]) == 1
        
        if not conf.buffer or not conf.stack or stack_at_root or next_already_dep:
            return -1
            
        idx_wi = conf.stack.pop(-1)
        idx_wj = conf.buffer[0]
        
        conf.arcs.append((idx_wj, relation, idx_wi))
        

    @staticmethod
    def right_arc(conf, relation):
        #print(conf)
        """
            :param configuration: is the current configuration
            :return : A new configuration or -1 if the pre-condition is not satisfied
        """
        if not conf.buffer or not conf.stack:
            return -1

        # You get this one for free! Use it as an example.

        idx_wi = conf.stack[-1]
        idx_wj = conf.buffer.pop(0)

        conf.stack.append(idx_wj)
        conf.arcs.append((idx_wi, relation, idx_wj))

    @staticmethod
    def reduce(conf):
        #print(conf)
        """
            :param configuration: is the current configuration
            :return : A new configuration or -1 if the pre-condition is not satisfied
        """
        next_already_dep = conf.stack and len([x for x in conf.arcs if x[2] == conf.stack[-1]]) == 1
        if not conf.stack or not next_already_dep:
            #print(conf)
            return -1
            
        conf.stack.pop(-1)

    @staticmethod
    def shift(conf):
        #print(conf)
        """
            :param configuration: is the current configuration
            :return : A new configuration or -1 if the pre-condition is not satisfied
        """
        if not conf.buffer:
            return -1
            
        conf.stack.append(conf.buffer.pop(0))
